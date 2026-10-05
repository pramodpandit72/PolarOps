from django.db import models
from django.utils import timezone
from datetime import timedelta


class Location(models.Model):
    LOCATION_TYPES = [
        ('Research Station', 'Research Station'),
        ('Expedition Camp', 'Expedition Camp'),
        ('Storage Facility', 'Storage Facility'),
        ('Supply Point', 'Supply Point'),
        ('Field Location', 'Field Location'),
    ]

    location_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES, default='Research Station')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.location_id})"


class Expedition(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    expedition_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='expeditions')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} [{self.expedition_id}]"


class Personnel(models.Model):
    ROLE_CHOICES = [
        ('Expedition Leader', 'Expedition Leader'),
        ('Researcher', 'Researcher'),
        ('Engineer', 'Engineer'),
        ('Logistics Coordinator', 'Logistics Coordinator'),
        ('Medical Officer', 'Medical Officer'),
        ('Technician', 'Technician'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Researcher')
    contact = models.CharField(max_length=100, blank=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, null=True, blank=True, related_name='personnel')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.role})"


class Asset(models.Model):
    CATEGORY_CHOICES = [
        ('Snowmobile', 'Snowmobile'),
        ('Generator', 'Generator'),
        ('Satellite Phone', 'Satellite Phone'),
        ('GPS Device', 'GPS Device'),
        ('Research Equipment', 'Research Equipment'),
        ('Heating System', 'Heating System'),
        ('Communication Equipment', 'Communication Equipment'),
        ('Protective Gear', 'Protective Gear'),
        ('Vehicle', 'Vehicle'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Damaged', 'Damaged'),
        ('Retired', 'Retired'),
    ]

    asset_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    serial_number = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Available')
    acquisition_date = models.DateField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.asset_id}]"

    @property
    def maintenance_status(self):
        """Returns tuple of (code, label, color_class) for maintenance alert."""
        if not self.next_maintenance_date:
            return ('ok', 'Maintenance Up to Date', 'emerald')
        
        today = timezone.now().date()
        if self.next_maintenance_date < today:
            return ('overdue', 'Maintenance Overdue', 'red')
        elif self.next_maintenance_date <= today + timedelta(days=14):
            return ('soon', 'Maintenance Soon', 'amber')
        return ('ok', 'Maintenance Up to Date', 'emerald')


class Supply(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Fuel', 'Fuel'),
        ('Medical Supplies', 'Medical Supplies'),
        ('Water', 'Water'),
        ('Batteries', 'Batteries'),
        ('Research Materials', 'Research Materials'),
        ('Emergency Equipment', 'Emergency Equipment'),
        ('Other', 'Other'),
    ]

    supply_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, default='Units')
    minimum_required_quantity = models.PositiveIntegerField(default=10)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplies')
    storage_location = models.CharField(max_length=150, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_required_quantity


class Logistics(models.Model):
    TRANSPORT_CHOICES = [
        ('Ski-Plane Air Drop', 'Ski-Plane Air Drop'),
        ('Twin Otter Cargo Flight', 'Twin Otter Cargo Flight'),
        ('Icebreaker Vessel', 'Icebreaker Vessel'),
        ('Snowcat Overland Convoy', 'Snowcat Overland Convoy'),
        ('Helicopter Sling', 'Helicopter Sling'),
        ('Snowmobile Sled', 'Snowmobile Sled'),
    ]

    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled'),
    ]

    shipment_id = models.CharField(max_length=50, unique=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, null=True, blank=True, related_name='logistics_records')
    item_description = models.CharField(max_length=200)
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    transport_method = models.CharField(max_length=50, choices=TRANSPORT_CHOICES, default='Twin Otter Cargo Flight')
    dispatch_date = models.DateField(null=True, blank=True)
    expected_arrival = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.shipment_id}: {self.item_description} ({self.status})"


class Maintenance(models.Model):
    TYPE_CHOICES = [
        ('Scheduled Service', 'Scheduled Service'),
        ('Pre-Departure Inspection', 'Pre-Departure Inspection'),
        ('Cold-Weather Overhaul', 'Cold-Weather Overhaul'),
        ('Emergency Repair', 'Emergency Repair'),
        ('Calibration', 'Calibration'),
    ]

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]

    maintenance_id = models.CharField(max_length=50, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Scheduled Service')
    description = models.TextField()
    maintenance_date = models.DateField()
    next_maintenance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.maintenance_id} - {self.asset.name} ({self.status})"


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    task_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_personnel = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date', '-created_at']

    def __str__(self):
        return f"{self.title} [{self.priority}]"


class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action}: {self.details} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
