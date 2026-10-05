from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from operations.models import (
    Location, Expedition, Personnel, Asset, Supply, Logistics, Maintenance, Task, ActivityLog
)


class Command(BaseCommand):
    help = 'Seeds initial realistic polar expedition data into MongoDB Atlas'

    def handle(self, *args, **options):
        self.stdout.write('Seeding PolarOps initial operational data...')

        # 1. Locations
        locations_data = [
            {
                'location_id': 'LOC-SVAL-01',
                'name': 'Ny-Ålesund Research Station',
                'region': 'Svalbard Archipelago (78°55′N)',
                'description': 'Northernmost permanent civilian research settlement in the world.',
                'latitude': '78.9235 N',
                'longitude': '11.9099 E',
                'location_type': 'Research Station',
            },
            {
                'location_id': 'LOC-GRN-02',
                'name': 'Summit Station Camp',
                'region': 'Greenland Ice Sheet (72°34′N)',
                'description': 'High-altitude year-round ice core and atmospheric research facility.',
                'latitude': '72.5800 N',
                'longitude': '38.4500 W',
                'location_type': 'Expedition Camp',
            },
            {
                'location_id': 'LOC-ANT-03',
                'name': 'McMurdo Base Station',
                'region': 'Ross Island, Antarctica (77°50′S)',
                'description': 'Primary logistics hub and scientific station on the Ross Ice Shelf.',
                'latitude': '77.8419 S',
                'longitude': '166.6863 E',
                'location_type': 'Research Station',
            },
            {
                'location_id': 'LOC-DEP-04',
                'name': 'Tromsø Polar Logistics Depot',
                'region': 'Northern Norway (69°39′N)',
                'description': 'Maritime transshipment staging hub and cold-storage facility.',
                'latitude': '69.6492 N',
                'longitude': '18.9553 E',
                'location_type': 'Storage Facility',
            },
            {
                'location_id': 'LOC-FLD-05',
                'name': 'Fram Strait Field Camp',
                'region': 'East Greenland Sea (80°10′N)',
                'description': 'Temporary sea-ice acoustic hydrophone array monitoring outpost.',
                'latitude': '80.1667 N',
                'longitude': '0.0000 E',
                'location_type': 'Field Location',
            },
        ]

        loc_objs = {}
        for l in locations_data:
            loc, _ = Location.objects.update_or_create(location_id=l['location_id'], defaults=l)
            loc_objs[l['location_id']] = loc

        self.stdout.write(f'  Created/verified {len(loc_objs)} Locations.')

        # 2. Expeditions
        today = timezone.now().date()
        expeditions_data = [
            {
                'expedition_id': 'EXP-2026-01',
                'name': 'Arctic Sea-Ice Dynamics Campaign',
                'description': 'Multi-week deployment measuring winter ice thickness and thermal heat flux using autonomous submersibles.',
                'objective': 'Map multi-year ice decline in sector Fram-4 and calibrate satellite radar altimetry.',
                'location': loc_objs['LOC-SVAL-01'],
                'start_date': today - timedelta(days=20),
                'end_date': today + timedelta(days=25),
                'status': 'Active',
            },
            {
                'expedition_id': 'EXP-2026-02',
                'name': 'Greenland Deep Ice Core Drilling',
                'description': 'Deep firn core extraction to analyze paleoclimatic methane isotopes over the past 12,000 years.',
                'objective': 'Extract 800m of continuous ice core and maintain clean-room thermal storage.',
                'location': loc_objs['LOC-GRN-02'],
                'start_date': today + timedelta(days=15),
                'end_date': today + timedelta(days=90),
                'status': 'Planned',
            },
            {
                'expedition_id': 'EXP-2026-03',
                'name': 'Ross Ice Shelf Seismic Traverse',
                'description': 'Ground-penetrating radar and explosive seismic reflection traverse across sub-ice cavity channels.',
                'objective': 'Survey basal melting rates along grounding lines and assess tectonic bedrock stability.',
                'location': loc_objs['LOC-ANT-03'],
                'start_date': today - timedelta(days=45),
                'end_date': today + timedelta(days=10),
                'status': 'Active',
            },
            {
                'expedition_id': 'EXP-2026-04',
                'name': 'Polar Oceanographic Acoustic Survey',
                'description': 'High-latitude ocean listening array deployment across Fram Strait deep sea trenches.',
                'objective': 'Record marine mammal migration acoustic patterns under permanent ice canopy.',
                'location': loc_objs['LOC-FLD-05'],
                'start_date': today - timedelta(days=80),
                'end_date': today - timedelta(days=10),
                'status': 'Completed',
            },
        ]

        exp_objs = {}
        for e in expeditions_data:
            exp, _ = Expedition.objects.update_or_create(expedition_id=e['expedition_id'], defaults=e)
            exp_objs[e['expedition_id']] = exp

        self.stdout.write(f'  Created/verified {len(exp_objs)} Expeditions.')

        # 3. Personnel
        personnel_data = [
            {
                'name': 'Dr. Astrid Lindqvist',
                'email': 'astrid.lindqvist@polarops.local',
                'role': 'Expedition Leader',
                'contact': '+47 79 02 33 01 / Iridium #411',
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'Active',
            },
            {
                'name': 'Lars Torvald',
                'email': 'lars.torvald@polarops.local',
                'role': 'Engineer',
                'contact': '+47 79 02 33 02 / UHF Ch. 4',
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'Active',
            },
            {
                'name': 'Dr. Elena Rostova',
                'email': 'elena.rostova@polarops.local',
                'role': 'Researcher',
                'contact': '+45 38 14 20 10 / Sat-Phone #09',
                'expedition': exp_objs['EXP-2026-02'],
                'status': 'Active',
            },
            {
                'name': 'Captain Marcus Vance',
                'email': 'marcus.vance@polarops.local',
                'role': 'Logistics Coordinator',
                'contact': '+1 303 555 0192 / SatCom Alpha',
                'expedition': exp_objs['EXP-2026-03'],
                'status': 'Active',
            },
            {
                'name': 'Dr. Noah Gallagher',
                'email': 'noah.gallagher@polarops.local',
                'role': 'Medical Officer',
                'contact': '+1 303 555 0198 / Station Medline',
                'expedition': exp_objs['EXP-2026-03'],
                'status': 'Active',
            },
            {
                'name': 'Kari Mikkelsen',
                'email': 'kari.mikkelsen@polarops.local',
                'role': 'Technician',
                'contact': '+47 79 02 33 08 / Radio #2',
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'Active',
            },
            {
                'name': 'Sven Hedin',
                'email': 'sven.hedin@polarops.local',
                'role': 'Technician',
                'contact': '+46 8 123 456 / Standby',
                'expedition': None,
                'status': 'On Leave',
            },
        ]

        for p in personnel_data:
            Personnel.objects.update_or_create(email=p['email'], defaults=p)

        self.stdout.write(f'  Created/verified {len(personnel_data)} Personnel records.')

        # 4. Assets
        assets_data = [
            {
                'asset_id': 'AST-SNOW-01',
                'name': 'Yamaha VK540 Arctic Utility Snowmobile A',
                'category': 'Snowmobile',
                'serial_number': 'YAM-VK540-8841',
                'location': loc_objs['LOC-SVAL-01'],
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'In Use',
                'acquisition_date': date(2023, 4, 15),
                'last_maintenance_date': today - timedelta(days=40),
                'next_maintenance_date': today + timedelta(days=20),
            },
            {
                'asset_id': 'AST-SNOW-02',
                'name': 'Yamaha VK540 Arctic Utility Snowmobile B',
                'category': 'Snowmobile',
                'serial_number': 'YAM-VK540-8842',
                'location': loc_objs['LOC-SVAL-01'],
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'Available',
                'acquisition_date': date(2023, 4, 15),
                'last_maintenance_date': today - timedelta(days=60),
                'next_maintenance_date': today + timedelta(days=5),  # soon
            },
            {
                'asset_id': 'AST-GEN-01',
                'name': 'Cummins 45kVA Arctic-Enclosed Diesel Generator',
                'category': 'Generator',
                'serial_number': 'CUM-DK-45901',
                'location': loc_objs['LOC-GRN-02'],
                'expedition': exp_objs['EXP-2026-02'],
                'status': 'Under Maintenance',
                'acquisition_date': date(2022, 8, 10),
                'last_maintenance_date': today - timedelta(days=120),
                'next_maintenance_date': today - timedelta(days=5),  # overdue
            },
            {
                'asset_id': 'AST-SAT-01',
                'name': 'Iridium Pilot Extreme Marine & Field Satellite Terminal',
                'category': 'Satellite Phone',
                'serial_number': 'IRD-EXT-00441',
                'location': loc_objs['LOC-ANT-03'],
                'expedition': exp_objs['EXP-2026-03'],
                'status': 'In Use',
                'acquisition_date': date(2024, 1, 20),
                'last_maintenance_date': today - timedelta(days=30),
                'next_maintenance_date': today + timedelta(days=60),
            },
            {
                'asset_id': 'AST-RES-01',
                'name': 'Kowari Deep Thermal Ice Core Drill Rig',
                'category': 'Research Equipment',
                'serial_number': 'KOW-DRL-02',
                'location': loc_objs['LOC-DEP-04'],
                'expedition': exp_objs['EXP-2026-02'],
                'status': 'Available',
                'acquisition_date': date(2023, 11, 5),
                'last_maintenance_date': today - timedelta(days=15),
                'next_maintenance_date': today + timedelta(days=90),
            },
            {
                'asset_id': 'AST-HEAT-01',
                'name': 'Webasto Air Top 5500 Multi-Tent Heaters (Pair)',
                'category': 'Heating System',
                'serial_number': 'WEB-AT-5520',
                'location': loc_objs['LOC-SVAL-01'],
                'expedition': exp_objs['EXP-2026-01'],
                'status': 'In Use',
                'acquisition_date': date(2023, 2, 18),
                'last_maintenance_date': today - timedelta(days=50),
                'next_maintenance_date': today + timedelta(days=25),
            },
            {
                'asset_id': 'AST-VEH-01',
                'name': 'Hägglunds Bv206 Articulated All-Terrain Carrier',
                'category': 'Vehicle',
                'serial_number': 'BV206-MIL-109',
                'location': loc_objs['LOC-ANT-03'],
                'expedition': exp_objs['EXP-2026-03'],
                'status': 'In Use',
                'acquisition_date': date(2021, 6, 30),
                'last_maintenance_date': today - timedelta(days=85),
                'next_maintenance_date': today + timedelta(days=7),  # soon
            },
        ]

        asset_objs = {}
        for a in assets_data:
            ast, _ = Asset.objects.update_or_create(asset_id=a['asset_id'], defaults=a)
            asset_objs[a['asset_id']] = ast

        self.stdout.write(f'  Created/verified {len(asset_objs)} Asset records.')

        # 5. Supplies
        supplies_data = [
            {
                'supply_id': 'SUP-FUEL-01',
                'name': 'Jet-A1 Aviation & Field Generator Fuel',
                'category': 'Fuel',
                'quantity': 3500,
                'unit': 'Liters',
                'minimum_required_quantity': 2000,
                'location': loc_objs['LOC-SVAL-01'],
                'storage_location': 'Bunker Fuel Depot 1',
                'expiry_date': today + timedelta(days=365),
            },
            {
                'supply_id': 'SUP-FUEL-02',
                'name': 'Sub-Zero Low-Viscosity 2-Stroke Synthetic Engine Oil',
                'category': 'Fuel',
                'quantity': 18,
                'unit': 'Liters',
                'minimum_required_quantity': 25,  # LOW STOCK
                'location': loc_objs['LOC-SVAL-01'],
                'storage_location': 'Workshop Cabinet 4',
                'expiry_date': today + timedelta(days=500),
            },
            {
                'supply_id': 'SUP-MED-01',
                'name': 'Hypothermia & Cold Trauma Advanced Medical Kits',
                'category': 'Medical Supplies',
                'quantity': 4,
                'unit': 'Kits',
                'minimum_required_quantity': 5,  # LOW STOCK
                'location': loc_objs['LOC-GRN-02'],
                'storage_location': 'Station Infirmary Safe',
                'expiry_date': today + timedelta(days=180),
            },
            {
                'supply_id': 'SUP-FOOD-01',
                'name': 'Vacuum-Sealed High-Calorie Polar Ration Packs (5000 kcal)',
                'category': 'Food',
                'quantity': 450,
                'unit': 'Packs',
                'minimum_required_quantity': 200,
                'location': loc_objs['LOC-ANT-03'],
                'storage_location': 'Commissary Dry Storage',
                'expiry_date': today + timedelta(days=720),
            },
            {
                'supply_id': 'SUP-BAT-01',
                'name': 'Cold-Resistant LiFePO4 12V 100Ah Field Batteries',
                'category': 'Batteries',
                'quantity': 8,
                'unit': 'Units',
                'minimum_required_quantity': 10,  # LOW STOCK
                'location': loc_objs['LOC-DEP-04'],
                'storage_location': 'Battery Charging Bay',
                'expiry_date': today + timedelta(days=900),
            },
            {
                'supply_id': 'SUP-RES-01',
                'name': 'Polyethylene Ice Core Storage Sleeves (1-meter)',
                'category': 'Research Materials',
                'quantity': 600,
                'unit': 'Units',
                'minimum_required_quantity': 150,
                'location': loc_objs['LOC-DEP-04'],
                'storage_location': 'Warehouse Racks B-12',
                'expiry_date': None,
            },
        ]

        for s in supplies_data:
            Supply.objects.update_or_create(supply_id=s['supply_id'], defaults=s)

        self.stdout.write(f'  Created/verified {len(supplies_data)} Supply inventory records.')

        # 6. Logistics
        logistics_data = [
            {
                'shipment_id': 'LOG-AIR-2601',
                'expedition': exp_objs['EXP-2026-01'],
                'item_description': 'Emergency Replacement Fuel Filters & Spare Snowmobile Belts',
                'origin': 'Tromsø Polar Logistics Depot',
                'destination': 'Ny-Ålesund Research Station',
                'transport_method': 'Twin Otter Cargo Flight',
                'dispatch_date': today - timedelta(days=2),
                'expected_arrival': today + timedelta(days=1),
                'status': 'In Transit',
            },
            {
                'shipment_id': 'LOG-ICE-2602',
                'expedition': exp_objs['EXP-2026-03'],
                'item_description': 'Deep Seismic Explosive Caps & Geophone Strings',
                'origin': 'Christchurch Marine Depot',
                'destination': 'McMurdo Base Station',
                'transport_method': 'Icebreaker Vessel',
                'dispatch_date': today - timedelta(days=14),
                'expected_arrival': today + timedelta(days=4),
                'status': 'In Transit',
            },
            {
                'shipment_id': 'LOG-AIR-2603',
                'expedition': exp_objs['EXP-2026-02'],
                'item_description': 'Deep Firn Core Drill Bits and Ethylene Glycol Thermal Fluid',
                'origin': 'Kangerlussuaq Airport',
                'destination': 'Summit Station Camp',
                'transport_method': 'Ski-Plane Air Drop',
                'dispatch_date': today + timedelta(days=8),
                'expected_arrival': today + timedelta(days=12),
                'status': 'Planned',
            },
        ]

        for l in logistics_data:
            Logistics.objects.update_or_create(shipment_id=l['shipment_id'], defaults=l)

        self.stdout.write(f'  Created/verified {len(logistics_data)} Logistics records.')

        # 7. Maintenance
        maint_data = [
            {
                'maintenance_id': 'MNT-2026-01',
                'asset': asset_objs['AST-GEN-01'],
                'maintenance_type': 'Cold-Weather Overhaul',
                'description': 'Replace glow plugs, flush fuel injector lines, and replace engine block silicone heater gaskets.',
                'maintenance_date': today - timedelta(days=5),
                'next_maintenance_date': today + timedelta(days=90),
                'status': 'In Progress',
                'notes': 'Waiting on specialized gasket shipment from Tromsø.',
            },
            {
                'maintenance_id': 'MNT-2026-02',
                'asset': asset_objs['AST-SNOW-02'],
                'maintenance_type': 'Pre-Departure Inspection',
                'description': 'Tension drive track, verify steering ski carbide runners, replace spark plugs.',
                'maintenance_date': today - timedelta(days=1),
                'next_maintenance_date': today + timedelta(days=30),
                'status': 'Scheduled',
                'notes': 'Inspection required prior to second traverse wave.',
            },
            {
                'maintenance_id': 'MNT-2026-03',
                'asset': asset_objs['AST-VEH-01'],
                'maintenance_type': 'Scheduled Service',
                'description': '100-hour hydraulic fluid change and bogie wheel bearing lubrication with sub-zero grease.',
                'maintenance_date': today + timedelta(days=6),
                'next_maintenance_date': today + timedelta(days=120),
                'status': 'Scheduled',
                'notes': 'Schedule with mechanic team at McMurdo garage.',
            },
        ]

        for m in maint_data:
            Maintenance.objects.update_or_create(maintenance_id=m['maintenance_id'], defaults=m)

        self.stdout.write(f'  Created/verified {len(maint_data)} Maintenance logs.')

        # 8. Tasks
        p_astrid = Personnel.objects.get(email='astrid.lindqvist@polarops.local')
        p_lars = Personnel.objects.get(email='lars.torvald@polarops.local')
        p_vance = Personnel.objects.get(email='marcus.vance@polarops.local')

        tasks_data = [
            {
                'task_id': 'TSK-2601',
                'title': 'Calibrate Radar Ice-Sounding Altimeter on Snowmobile Alpha',
                'description': 'Run zero-calibration test on 400 MHz antenna against known benchmark ice shelf stake.',
                'assigned_personnel': p_lars,
                'expedition': exp_objs['EXP-2026-01'],
                'priority': 'High',
                'due_date': today + timedelta(days=2),
                'status': 'In Progress',
            },
            {
                'task_id': 'TSK-2602',
                'title': 'Submit Weekly Polar Bear Watch & Camp Security Log',
                'description': 'Upload perimeter flare tripwire check and flare gun inventory log to station server.',
                'assigned_personnel': p_astrid,
                'expedition': exp_objs['EXP-2026-01'],
                'priority': 'Critical',
                'due_date': today + timedelta(days=1),
                'status': 'Pending',
            },
            {
                'task_id': 'TSK-2603',
                'title': 'Pre-position Winter Fuel Caches along Traverse Waypoint B',
                'description': 'Transport four 200L drums of Jet-A1 to waypoint Bravo using Bv206 carrier.',
                'assigned_personnel': p_vance,
                'expedition': exp_objs['EXP-2026-03'],
                'priority': 'Critical',
                'due_date': today + timedelta(days=5),
                'status': 'Pending',
            },
            {
                'task_id': 'TSK-2604',
                'title': 'Inspect Backup Satellite Dome De-Icing Coils',
                'description': 'Ensure heating elements activate automatically when ambient temp drops past -30°C.',
                'assigned_personnel': p_lars,
                'expedition': exp_objs['EXP-2026-01'],
                'priority': 'Medium',
                'due_date': today + timedelta(days=7),
                'status': 'Pending',
            },
            {
                'task_id': 'TSK-2605',
                'title': 'Inspect Firn Drill Pressure Chamber Sensors',
                'description': 'Verify pressure transducers in thermal drill core barrel are sealed against brine leakage.',
                'assigned_personnel': None,
                'expedition': exp_objs['EXP-2026-02'],
                'priority': 'Medium',
                'due_date': today - timedelta(days=3),
                'status': 'Completed',
            },
        ]

        for t in tasks_data:
            Task.objects.update_or_create(task_id=t['task_id'], defaults=t)

        self.stdout.write(f'  Created/verified {len(tasks_data)} Tasks.')

        # 9. Activity Logs
        ActivityLog.objects.all().delete()
        activities = [
            ('Expedition Created', 'Arctic Sea-Ice Dynamics Campaign [EXP-2026-01] registered at Ny-Ålesund.'),
            ('Asset Deployed', 'Yamaha VK540 Snowmobile Unit A assigned to field operations.'),
            ('Personnel Assigned', 'Dr. Astrid Lindqvist designated as Expedition Leader for EXP-2026-01.'),
            ('Supply Alert', 'Sub-Zero Synthetic Engine Oil dropped below minimum reserve threshold (18L remaining).'),
            ('Task Scheduled', 'Perimeter Polar Bear Watch & Safety Log assigned with Critical priority.'),
            ('Logistics Dispatched', 'Twin Otter Cargo Flight LOG-AIR-2601 en route from Tromsø to Svalbard.'),
        ]

        for action, details in activities:
            ActivityLog.objects.create(action=action, details=details)

        self.stdout.write(self.style.SUCCESS('Successfully seeded complete PolarOps operational dataset!'))
