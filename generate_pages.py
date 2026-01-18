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
    
    # Check if accommodation section should be shown
    has_accommodation = ('accommodation_message' in attendee and attendee['accommodation_message']) or \
                       ('accommodation' in attendee and attendee['accommodation']) or \
                       attendee['name'] == 'Kathy'
    
    # Pattern to match the entire accommodation section block including the hr before and after
    accommodation_block_pattern = r'      <hr>\s*{% if accommodation_message or accommodation or name == "Kathy" %}.*?<hr>\s*{% endif %}\s*'
    
    if not has_accommodation:
        # Remove entire accommodation section including the hr before and after it
        rendered = re.sub(
            accommodation_block_pattern,
            '',
            rendered,
            flags=re.DOTALL
        )
    else:
        # Handle accommodation section content
        if 'accommodation_message' in attendee and attendee['accommodation_message']:
            # Custom accommodation message
            accommodation_content = f"        <p>{attendee['accommodation_message']}</p>"
        elif 'accommodation' in attendee and attendee['accommodation']:
            # Standard accommodation with host
            accommodation_content = f"        <p>Hey {attendee['name']}! Thanks again for joining, we look forward to having you here. You should have received a personal message from us regarding your accommodation. We have planned your stay with: <strong>{attendee['accommodation']}</strong></p>\n        <p>Please let us know if this is okay for you.</p>"
        else:
            # Default coming soon message (for Kathy)
            accommodation_content = '        <div class="coming-soon">Coming soon: Accommodation details will be added here if you are coming from outside Darmstadt.</div>'
        
        # Replace the if/elif/else block inside the section
        inner_pattern = r'{% if accommodation_message %}.*?{% elif accommodation %}.*?{% else %}.*?{% endif %}'
        rendered = re.sub(
            inner_pattern,
            accommodation_content,
            rendered,
            flags=re.DOTALL
        )
        
        # Remove the outer if condition, keep the section and hr
        rendered = re.sub(
            r'      {% if accommodation_message or accommodation or name == "Kathy" %}',
            '',
            rendered
        )
        rendered = re.sub(
            r'      {% endif %}',
            '',
            rendered
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
