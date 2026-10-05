from django import forms
from .models import (
    Location, Expedition, Personnel, Asset, Supply, Logistics, Maintenance, Task
)

TAILWIND_INPUT = (
    "w-full px-3.5 py-2.5 rounded-lg border border-slate-300 dark:border-[#243B5A] "
    "bg-white dark:bg-[#101D32] text-[#0B1628] dark:text-[#F8FAFC] "
    "focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 text-sm transition-all"
)

TAILWIND_SELECT = (
    "w-full px-3.5 py-2.5 rounded-lg border border-slate-300 dark:border-[#243B5A] "
    "bg-white dark:bg-[#101D32] text-[#0B1628] dark:text-[#F8FAFC] "
    "focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 text-sm transition-all"
)

TAILWIND_TEXTAREA = (
    "w-full px-3.5 py-2.5 rounded-lg border border-slate-300 dark:border-[#243B5A] "
    "bg-white dark:bg-[#101D32] text-[#0B1628] dark:text-[#F8FAFC] "
    "focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 text-sm transition-all"
)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_id', 'name', 'region', 'location_type', 'latitude', 'longitude', 'description']
        widgets = {
            'location_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. LOC-SVAL-01'}),
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Ny-Ålesund Research Station'}),
            'region': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Svalbard Archipelago (78°55′N)'}),
            'location_type': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'latitude': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. 78.9235 N'}),
            'longitude': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. 11.9099 E'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3, 'placeholder': 'Operational facility notes and coordinates...'}),
        }


class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['expedition_id', 'name', 'location', 'start_date', 'end_date', 'status', 'objective', 'description']
        widgets = {
            'expedition_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. EXP-2026-05'}),
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Polar Ice Core Analysis Traverse'}),
            'location': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'start_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'objective': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2, 'placeholder': 'Primary scientific or logistical objective...'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3, 'placeholder': 'Detailed operational brief...'}),
        }


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['name', 'email', 'role', 'contact', 'expedition', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Dr. Astrid Lindqvist'}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'name@polarops.local'}),
            'role': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'contact': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. +47 79 02 33 01 / Sat-Phone #04'}),
            'expedition': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'asset_id', 'name', 'category', 'serial_number', 'location', 
            'expedition', 'status', 'acquisition_date', 'last_maintenance_date', 'next_maintenance_date'
        ]
        widgets = {
            'asset_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. AST-SNOW-05'}),
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Yamaha VK540 Snowmobile Unit C'}),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'serial_number': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. SN-8849-AK'}),
            'location': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'expedition': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'acquisition_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'last_maintenance_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
        }


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['supply_id', 'name', 'category', 'quantity', 'unit', 'minimum_required_quantity', 'location', 'storage_location', 'expiry_date']
        widgets = {
            'supply_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. SUP-FUEL-09'}),
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. High-Calorie Polar Ration Packs'}),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'quantity': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'unit': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Liters, Packs, Kits, Units'}),
            'minimum_required_quantity': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'location': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'storage_location': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Hangar 2, Shelf B-4'}),
            'expiry_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
        }


class LogisticsForm(forms.ModelForm):
    class Meta:
        model = Logistics
        fields = ['shipment_id', 'expedition', 'item_description', 'origin', 'destination', 'transport_method', 'dispatch_date', 'expected_arrival', 'status']
        widgets = {
            'shipment_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. LOG-AIR-2605'}),
            'expedition': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'item_description': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Replacement Generator Fuel Injectors'}),
            'origin': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Tromsø Logistics Depot'}),
            'destination': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Summit Station Greenland'}),
            'transport_method': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'dispatch_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'expected_arrival': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
        }


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['maintenance_id', 'asset', 'maintenance_type', 'maintenance_date', 'next_maintenance_date', 'status', 'description', 'notes']
        widgets = {
            'maintenance_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. MNT-2026-12'}),
            'asset': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'maintenance_type': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'maintenance_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2, 'placeholder': 'Work performed or scheduled service tasks...'}),
            'notes': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2, 'placeholder': 'Observations, technician initials, parts used...'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_id', 'title', 'assigned_personnel', 'expedition', 'priority', 'due_date', 'status', 'description']
        widgets = {
            'task_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. TSK-2610'}),
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Pre-Departure Weather Station Calibration'}),
            'assigned_personnel': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'expedition': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'priority': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'due_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3, 'placeholder': 'Operational task details and instructions...'}),
        }
