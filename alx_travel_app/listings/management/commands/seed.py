#!/usr/bin/env python3
"""
Management command to seed the database with sample data
"""

from django.core.management.base import BaseCommand
from listings.models import Listing
import random


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        sample_data = [
            {
                "title": "Beachfront Bungalow",
                "description": "Enjoy ocean views and relaxing vibes.",
                "location": "Zanzibar, Tanzania",
                "price_per_night": 120.00,
                "is_available": True
            },
            {
                "title": "Mountain Cabin Retreat",
                "description": "Secluded and cozy cabin in the mountains.",
                "location": "Drakensberg, South Africa",
                "price_per_night": 95.50,
                "is_available": True
            },
            {
                "title": "Modern City Apartment",
                "description": "Close to everything, ideal for city explorers.",
                "location": "Nairobi, Kenya",
                "price_per_night": 80.00,
                "is_available": False
            }
        ]

        for data in sample_data:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('✅ Database successfully seeded with sample listings!'))
