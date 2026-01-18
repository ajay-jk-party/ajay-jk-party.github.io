#!/usr/bin/env python3
"""
Script to generate personal attendee pages from a template and JSON data.
Run this script whenever you update the template or attendee data.

Usage: python3 generate_pages.py
"""

import json
import os
import re

def load_template():
    """Load the Jinja-style template."""
    with open('templates/personal_page.html', 'r') as f:
        return f.read()

def load_attendees():
    """Load attendee data from JSON."""
    with open('attendees.json', 'r') as f:
        return json.load(f)['attendees']

def render_template(template, attendee):
    """Simple template rendering (replaces {{ name }}, {{ accommodation }}, and {{ accommodation_message }} with actual values)."""
    rendered = template.replace('{{ name }}', attendee['name'])
    
    # Handle accommodation section - check for custom message first, then accommodation, then default
    accommodation_section_pattern = r'{% if accommodation_message %}.*?{% elif accommodation %}.*?{% else %}.*?{% endif %}'
    
    if 'accommodation_message' in attendee and attendee['accommodation_message']:
        # Custom accommodation message
        accommodation_text = f"<p>{attendee['accommodation_message']}</p>"
        rendered = re.sub(
            accommodation_section_pattern,
            accommodation_text,
            rendered,
            flags=re.DOTALL
        )
    elif 'accommodation' in attendee and attendee['accommodation']:
        # Standard accommodation with host
        accommodation_text = f"<p>Hey {attendee['name']}! Thanks again for joining, we look forward to having you here. You should have received a personal message from us regarding your accommodation. We have planned your stay with: <strong>{attendee['accommodation']}</strong></p>\n        <p>Please let us know if this is okay for you.</p>"
        rendered = re.sub(
            accommodation_section_pattern,
            accommodation_text,
            rendered,
            flags=re.DOTALL
        )
    else:
        # Default coming soon message
        rendered = re.sub(
            accommodation_section_pattern,
            '<div class="coming-soon">Coming soon: Accommodation details will be added here if you are coming from outside Darmstadt.</div>',
            rendered,
            flags=re.DOTALL
        )
    
    return rendered

def generate_pages():
    """Generate all personal pages from the template."""
    template = load_template()
    attendees = load_attendees()
    
    # Create p directory if it doesn't exist
    os.makedirs('p', exist_ok=True)
    
    generated = 0
    for attendee in attendees:
        # Create directory for this attendee
        dir_path = f"p/{attendee['slug']}"
        os.makedirs(dir_path, exist_ok=True)
        
        # Render template with attendee data
        html = render_template(template, attendee)
        
        # Write the page
        with open(f"{dir_path}/index.html", 'w') as f:
            f.write(html)
        
        generated += 1
        print(f"Generated: {dir_path}/index.html")
    
    print(f"\nTotal pages generated: {generated}")

if __name__ == '__main__':
    generate_pages()
