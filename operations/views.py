from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    Location, Expedition, Personnel, Asset, Supply, Logistics, Maintenance, Task, ActivityLog
)
from .forms import (
    LocationForm, ExpeditionForm, PersonnelForm, AssetForm, SupplyForm, LogisticsForm, MaintenanceForm, TaskForm
)


def log_activity(action, details):
    ActivityLog.objects.create(action=action, details=details)


# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------
@login_required
def dashboard_view(request):
    """Main Operational Control Center."""
    today = timezone.now().date()

    # Database calculated metrics
    active_expeditions_count = Expedition.objects.filter(status='Active').count()
    personnel_count = Personnel.objects.filter(status='Active').count()
    operational_assets_count = Asset.objects.filter(status__in=['Available', 'In Use']).count()
    pending_tasks_count = Task.objects.exclude(status='Completed').count()
    
    # Calculate low stock dynamically
    all_supplies = list(Supply.objects.all())
    low_stock_items = [s for s in all_supplies if s.is_low_stock]
    low_stock_count = len(low_stock_items)

    # Calculate maintenance due
    all_assets = list(Asset.objects.all())
    maintenance_alerts = [a for a in all_assets if a.maintenance_status[0] in ['overdue', 'soon']]
    maintenance_due_count = len(maintenance_alerts)

    # Operational overview tables
    active_expeditions = Expedition.objects.filter(status='Active')[:6]
    recent_activities = ActivityLog.objects.all()[:6]
    critical_tasks = Task.objects.filter(priority__in=['Critical', 'High']).exclude(status='Completed')[:5]

    context = {
        'active_expeditions_count': active_expeditions_count,
        'personnel_count': personnel_count,
        'operational_assets_count': operational_assets_count,
        'pending_tasks_count': pending_tasks_count,
        'low_stock_count': low_stock_count,
        'maintenance_due_count': maintenance_due_count,
        'active_expeditions': active_expeditions,
        'recent_activities': recent_activities,
        'critical_tasks': critical_tasks,
        'low_stock_items': low_stock_items[:4],
        'maintenance_alerts': maintenance_alerts[:4],
        'today': today,
    }
    return render(request, 'dashboard.html', context)


# -------------------------------------------------------------------
# EXPEDITIONS
# -------------------------------------------------------------------
@login_required
def expedition_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    expeditions = Expedition.objects.all()
    if q:
        expeditions = expeditions.filter(
            Q(name__icontains=q) | Q(expedition_id__icontains=q) | Q(objective__icontains=q)
        )
    if status:
        expeditions = expeditions.filter(status=status)

    context = {
        'expeditions': expeditions,
        'q': q,
        'status_filter': status,
        'status_choices': Expedition.STATUS_CHOICES,
    }
    return render(request, 'operations/expedition_list.html', context)


@login_required
def expedition_detail(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    assigned_personnel = expedition.personnel.all()
    assigned_assets = expedition.assets.all()
    assigned_tasks = expedition.tasks.all()
    logistics = expedition.logistics_records.all()

    context = {
        'expedition': expedition,
        'assigned_personnel': assigned_personnel,
        'assigned_assets': assigned_assets,
        'assigned_tasks': assigned_tasks,
        'logistics': logistics,
    }
    return render(request, 'operations/expedition_detail.html', context)


@login_required
def expedition_create(request):
    if request.method == 'POST':
        form = ExpeditionForm(request.POST)
        if form.is_valid():
            exp = form.save()
            log_activity('Expedition Created', f"{exp.name} [{exp.expedition_id}] was created.")
            messages.success(request, f"Expedition '{exp.name}' created successfully.")
            return redirect('operations:expedition_detail', pk=exp.pk)
    else:
        form = ExpeditionForm()
    return render(request, 'operations/expedition_form.html', {'form': form, 'title': 'Create New Expedition'})


@login_required
def expedition_edit(request, pk):
    exp = get_object_or_404(Expedition, pk=pk)
    if request.method == 'POST':
        form = ExpeditionForm(request.POST, instance=exp)
        if form.is_valid():
            exp = form.save()
            log_activity('Expedition Updated', f"{exp.name} was updated.")
            messages.success(request, f"Expedition '{exp.name}' updated successfully.")
            return redirect('operations:expedition_detail', pk=exp.pk)
    else:
        form = ExpeditionForm(instance=exp)
    return render(request, 'operations/expedition_form.html', {'form': form, 'title': f"Edit {exp.name}", 'expedition': exp})


@login_required
def expedition_delete(request, pk):
    exp = get_object_or_404(Expedition, pk=pk)
    if request.method == 'POST':
        name = exp.name
        exp.delete()
        log_activity('Expedition Deleted', f"Expedition '{name}' was removed.")
        messages.success(request, f"Expedition '{name}' deleted successfully.")
        return redirect('operations:expedition_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Expedition: {exp.name}",
        'cancel_url': 'operations:expedition_list'
    })


# -------------------------------------------------------------------
# PERSONNEL
# -------------------------------------------------------------------
@login_required
def personnel_list(request):
    q = request.GET.get('q', '').strip()
    role = request.GET.get('role', '').strip()
    status = request.GET.get('status', '').strip()

    personnel = Personnel.objects.all()
    if q:
        personnel = personnel.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(contact__icontains=q))
    if role:
        personnel = personnel.filter(role=role)
    if status:
        personnel = personnel.filter(status=status)

    context = {
        'personnel_list': personnel,
        'q': q,
        'role_filter': role,
        'status_filter': status,
        'role_choices': Personnel.ROLE_CHOICES,
        'status_choices': Personnel.STATUS_CHOICES,
    }
    return render(request, 'operations/personnel_list.html', context)


@login_required
def personnel_create(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            person = form.save()
            log_activity('Personnel Added', f"{person.name} ({person.role}) added to roster.")
            messages.success(request, f"Personnel '{person.name}' added successfully.")
            return redirect('operations:personnel_list')
    else:
        form = PersonnelForm()
    return render(request, 'operations/personnel_form.html', {'form': form, 'title': 'Register New Personnel'})


@login_required
def personnel_edit(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save()
            log_activity('Personnel Updated', f"{person.name} records updated.")
            messages.success(request, f"Personnel '{person.name}' updated successfully.")
            return redirect('operations:personnel_list')
    else:
        form = PersonnelForm(instance=person)
    return render(request, 'operations/personnel_form.html', {'form': form, 'title': f"Edit {person.name}", 'person': person})


@login_required
def personnel_delete(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        name = person.name
        person.delete()
        log_activity('Personnel Removed', f"{name} removed from personnel roster.")
        messages.success(request, f"Personnel '{name}' deleted successfully.")
        return redirect('operations:personnel_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Personnel: {person.name} ({person.role})",
        'cancel_url': 'operations:personnel_list'
    })


# -------------------------------------------------------------------
# ASSETS
# -------------------------------------------------------------------
@login_required
def asset_list(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()
    maint_filter = request.GET.get('maint', '').strip()

    assets = Asset.objects.all()
    if q:
        assets = assets.filter(Q(name__icontains=q) | Q(asset_id__icontains=q) | Q(serial_number__icontains=q))
    if category:
        assets = assets.filter(category=category)
    if status:
        assets = assets.filter(status=status)

    asset_list_data = list(assets)
    if maint_filter == 'attention':
        asset_list_data = [a for a in asset_list_data if a.maintenance_status[0] in ['overdue', 'soon']]

    context = {
        'assets': asset_list_data,
        'q': q,
        'category_filter': category,
        'status_filter': status,
        'maint_filter': maint_filter,
        'category_choices': Asset.CATEGORY_CHOICES,
        'status_choices': Asset.STATUS_CHOICES,
    }
    return render(request, 'operations/asset_list.html', context)


@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    maintenance_records = asset.maintenance_records.all()

    context = {
        'asset': asset,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'operations/asset_detail.html', context)


@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            log_activity('Asset Registered', f"Asset {asset.name} [{asset.asset_id}] registered.")
            messages.success(request, f"Asset '{asset.name}' registered successfully.")
            return redirect('operations:asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    return render(request, 'operations/asset_form.html', {'form': form, 'title': 'Register New Asset'})


@login_required
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            log_activity('Asset Updated', f"Asset {asset.name} updated.")
            messages.success(request, f"Asset '{asset.name}' updated successfully.")
            return redirect('operations:asset_detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'operations/asset_form.html', {'form': form, 'title': f"Edit {asset.name}", 'asset': asset})


@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        name = asset.name
        asset.delete()
        log_activity('Asset Deleted', f"Asset '{name}' removed from inventory.")
        messages.success(request, f"Asset '{name}' deleted successfully.")
        return redirect('operations:asset_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Asset: {asset.name} [{asset.asset_id}]",
        'cancel_url': 'operations:asset_list'
    })


# -------------------------------------------------------------------
# SUPPLIES
# -------------------------------------------------------------------
@login_required
def supply_list(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    low_stock = request.GET.get('low_stock', '')

    supplies = Supply.objects.all()
    if q:
        supplies = supplies.filter(Q(name__icontains=q) | Q(supply_id__icontains=q) | Q(storage_location__icontains=q))
    if category:
        supplies = supplies.filter(category=category)

    supplies_data = list(supplies)
    if low_stock == 'true':
        supplies_data = [s for s in supplies_data if s.is_low_stock]

    context = {
        'supplies': supplies_data,
        'q': q,
        'category_filter': category,
        'low_stock_filter': low_stock,
        'category_choices': Supply.CATEGORY_CHOICES,
    }
    return render(request, 'operations/supply_list.html', context)


@login_required
def supply_create(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save()
            log_activity('Supply Added', f"{supply.name} ({supply.quantity} {supply.unit}) added.")
            messages.success(request, f"Supply '{supply.name}' added successfully.")
            return redirect('operations:supply_list')
    else:
        form = SupplyForm()
    return render(request, 'operations/supply_form.html', {'form': form, 'title': 'Add Supply Item'})


@login_required
def supply_edit(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            supply = form.save()
            log_activity('Supply Updated', f"{supply.name} inventory updated.")
            messages.success(request, f"Supply '{supply.name}' updated successfully.")
            return redirect('operations:supply_list')
    else:
        form = SupplyForm(instance=supply)
    return render(request, 'operations/supply_form.html', {'form': form, 'title': f"Edit {supply.name}", 'supply': supply})


@login_required
def supply_delete(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    if request.method == 'POST':
        name = supply.name
        supply.delete()
        log_activity('Supply Deleted', f"Supply '{name}' removed from inventory.")
        messages.success(request, f"Supply '{name}' deleted successfully.")
        return redirect('operations:supply_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Supply: {supply.name} ({supply.quantity} {supply.unit})",
        'cancel_url': 'operations:supply_list'
    })


# -------------------------------------------------------------------
# LOGISTICS
# -------------------------------------------------------------------
@login_required
def logistics_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    shipments = Logistics.objects.all()
    if q:
        shipments = shipments.filter(
            Q(shipment_id__icontains=q) | Q(item_description__icontains=q) | 
            Q(origin__icontains=q) | Q(destination__icontains=q)
        )
    if status:
        shipments = shipments.filter(status=status)

    context = {
        'shipments': shipments,
        'q': q,
        'status_filter': status,
        'status_choices': Logistics.STATUS_CHOICES,
    }
    return render(request, 'operations/logistics_list.html', context)


@login_required
def logistics_create(request):
    if request.method == 'POST':
        form = LogisticsForm(request.POST)
        if form.is_valid():
            log = form.save()
            log_activity('Shipment Dispatched', f"Logistics record {log.shipment_id} scheduled.")
            messages.success(request, f"Logistics shipment '{log.shipment_id}' created successfully.")
            return redirect('operations:logistics_list')
    else:
        form = LogisticsForm()
    return render(request, 'operations/logistics_form.html', {'form': form, 'title': 'Create Logistics Shipment'})


@login_required
def logistics_edit(request, pk):
    log = get_object_or_404(Logistics, pk=pk)
    if request.method == 'POST':
        form = LogisticsForm(request.POST, instance=log)
        if form.is_valid():
            log = form.save()
            log_activity('Shipment Updated', f"Logistics {log.shipment_id} updated to {log.status}.")
            messages.success(request, f"Logistics shipment '{log.shipment_id}' updated successfully.")
            return redirect('operations:logistics_list')
    else:
        form = LogisticsForm(instance=log)
    return render(request, 'operations/logistics_form.html', {'form': form, 'title': f"Edit Shipment {log.shipment_id}", 'logistics': log})


@login_required
def logistics_delete(request, pk):
    log = get_object_or_404(Logistics, pk=pk)
    if request.method == 'POST':
        sid = log.shipment_id
        log.delete()
        log_activity('Shipment Deleted', f"Shipment '{sid}' removed.")
        messages.success(request, f"Logistics record '{sid}' deleted successfully.")
        return redirect('operations:logistics_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Logistics Shipment: {log.shipment_id} ({log.item_description})",
        'cancel_url': 'operations:logistics_list'
    })


# -------------------------------------------------------------------
# MAINTENANCE
# -------------------------------------------------------------------
@login_required
def maintenance_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    records = Maintenance.objects.all()
    if q:
        records = records.filter(Q(maintenance_id__icontains=q) | Q(asset__name__icontains=q) | Q(description__icontains=q))
    if status:
        records = records.filter(status=status)

    context = {
        'records': records,
        'q': q,
        'status_filter': status,
        'status_choices': Maintenance.STATUS_CHOICES,
    }
    return render(request, 'operations/maintenance_list.html', context)


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            m = form.save()
            log_activity('Maintenance Scheduled', f"{m.maintenance_id} for {m.asset.name} recorded.")
            messages.success(request, f"Maintenance record '{m.maintenance_id}' created successfully.")
            return redirect('operations:maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'operations/maintenance_form.html', {'form': form, 'title': 'Log Maintenance Record'})


@login_required
def maintenance_edit(request, pk):
    m = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=m)
        if form.is_valid():
            m = form.save()
            log_activity('Maintenance Updated', f"{m.maintenance_id} updated.")
            messages.success(request, f"Maintenance record '{m.maintenance_id}' updated successfully.")
            return redirect('operations:maintenance_list')
    else:
        form = MaintenanceForm(instance=m)
    return render(request, 'operations/maintenance_form.html', {'form': form, 'title': f"Edit {m.maintenance_id}", 'maintenance': m})


@login_required
def maintenance_delete(request, pk):
    m = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        mid = m.maintenance_id
        m.delete()
        log_activity('Maintenance Deleted', f"Maintenance log '{mid}' deleted.")
        messages.success(request, f"Maintenance record '{mid}' deleted successfully.")
        return redirect('operations:maintenance_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Maintenance Log: {m.maintenance_id} ({m.asset.name})",
        'cancel_url': 'operations:maintenance_list'
    })


# -------------------------------------------------------------------
# TASKS
# -------------------------------------------------------------------
@login_required
def task_list(request):
    q = request.GET.get('q', '').strip()
    priority = request.GET.get('priority', '').strip()
    status = request.GET.get('status', '').strip()

    tasks = Task.objects.all()
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(task_id__icontains=q) | Q(description__icontains=q))
    if priority:
        tasks = tasks.filter(priority=priority)
    if status:
        tasks = tasks.filter(status=status)

    context = {
        'tasks': tasks,
        'q': q,
        'priority_filter': priority,
        'status_filter': status,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'operations/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save()
            log_activity('Task Created', f"Task '{t.title}' created with priority {t.priority}.")
            messages.success(request, f"Task '{t.title}' created successfully.")
            return redirect('operations:task_list')
    else:
        form = TaskForm()
    return render(request, 'operations/task_form.html', {'form': form, 'title': 'Create Operational Task'})


@login_required
def task_edit(request, pk):
    t = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=t)
        if form.is_valid():
            t = form.save()
            log_activity('Task Updated', f"Task '{t.title}' updated.")
            messages.success(request, f"Task '{t.title}' updated successfully.")
            return redirect('operations:task_list')
    else:
        form = TaskForm(instance=t)
    return render(request, 'operations/task_form.html', {'form': form, 'title': f"Edit {t.title}", 'task': t})


@login_required
def task_toggle_complete(request, pk):
    t = get_object_or_404(Task, pk=pk)
    if t.status == 'Completed':
        t.status = 'Pending'
    else:
        t.status = 'Completed'
    t.save()
    log_activity('Task Status Changed', f"Task '{t.title}' marked as {t.status}.")
    messages.success(request, f"Task '{t.title}' marked as {t.status}.")
    return redirect('operations:task_list')


@login_required
def task_delete(request, pk):
    t = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = t.title
        t.delete()
        log_activity('Task Deleted', f"Task '{title}' removed.")
        messages.success(request, f"Task '{title}' deleted successfully.")
        return redirect('operations:task_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Task: {t.title} [{t.task_id}]",
        'cancel_url': 'operations:task_list'
    })


# -------------------------------------------------------------------
# LOCATIONS
# -------------------------------------------------------------------
@login_required
def location_list(request):
    q = request.GET.get('q', '').strip()
    loc_type = request.GET.get('type', '').strip()

    locations = Location.objects.all()
    if q:
        locations = locations.filter(Q(name__icontains=q) | Q(location_id__icontains=q) | Q(region__icontains=q))
    if loc_type:
        locations = locations.filter(location_type=loc_type)

    context = {
        'locations': locations,
        'q': q,
        'type_filter': loc_type,
        'type_choices': Location.LOCATION_TYPES,
    }
    return render(request, 'operations/location_list.html', context)


@login_required
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    expeditions = location.expeditions.all()
    assets = location.assets.all()
    supplies = location.supplies.all()

    context = {
        'location': location,
        'expeditions': expeditions,
        'assets': assets,
        'supplies': supplies,
    }
    return render(request, 'operations/location_detail.html', context)


@login_required
def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save()
            log_activity('Location Registered', f"Location {loc.name} registered.")
            messages.success(request, f"Location '{loc.name}' registered successfully.")
            return redirect('operations:location_detail', pk=loc.pk)
    else:
        form = LocationForm()
    return render(request, 'operations/location_form.html', {'form': form, 'title': 'Register Operational Location'})


@login_required
def location_edit(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=loc)
        if form.is_valid():
            loc = form.save()
            log_activity('Location Updated', f"Location {loc.name} updated.")
            messages.success(request, f"Location '{loc.name}' updated successfully.")
            return redirect('operations:location_detail', pk=loc.pk)
    else:
        form = LocationForm(instance=loc)
    return render(request, 'operations/location_form.html', {'form': form, 'title': f"Edit {loc.name}", 'location': loc})


@login_required
def location_delete(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        name = loc.name
        loc.delete()
        log_activity('Location Deleted', f"Location '{name}' removed.")
        messages.success(request, f"Location '{name}' deleted successfully.")
        return redirect('operations:location_list')
    return render(request, 'operations/confirm_delete.html', {
        'object_name': f"Location: {loc.name} [{loc.location_id}]",
        'cancel_url': 'operations:location_list'
    })
