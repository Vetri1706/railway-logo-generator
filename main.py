#!/usr/bin/env python3
"""
AI Logo Generator - Railway Backend
A revolutionary professional logo generation system
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn

# Image generation imports
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Professional Logo Generator
from PIL import Image, ImageDraw, ImageFont
import random
import math

app = FastAPI(
    title="AI Logo Generator API",
    description="Professional logo generation service with 6 design categories",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogoRequest(BaseModel):
    company_name: str
    industry: str = "technology"
    style: str = "modern"
    color_scheme: str = "blue"

class ProfessionalLogoGenerator:
    def __init__(self):
        self.categories = {
            'wordmark': self._generate_wordmark,
            'lettermark': self._generate_lettermark, 
            'pictorial': self._generate_pictorial,
            'abstract': self._generate_abstract,
            'combination': self._generate_combination,
            'emblem': self._generate_emblem
        }
        
        self.color_schemes = {
            'blue': ['#1e40af', '#3b82f6', '#60a5fa'],
            'red': ['#dc2626', '#ef4444', '#f87171'],
            'green': ['#16a34a', '#22c55e', '#4ade80'],
            'purple': ['#7c3aed', '#8b5cf6', '#a78bfa'],
            'orange': ['#ea580c', '#f97316', '#fb923c'],
            'dark': ['#1f2937', '#374151', '#6b7280'],
            'gold': ['#d97706', '#f59e0b', '#fbbf24']
        }

    def generate_professional_logo(self, company_name: str, industry: str = "technology", 
                                 style: str = "modern", color_scheme: str = "blue") -> str:
        """Generate a high-quality professional logo"""
        
        # Select category based on company name and industry
        category = self._select_optimal_category(company_name, industry, style)
        
        # Generate the logo
        logo_path = self.categories[category](company_name, industry, color_scheme)
        
        return logo_path

    def _select_optimal_category(self, company_name: str, industry: str, style: str) -> str:
        """Select the best logo category for the company"""
        name_length = len(company_name.split())
        
        # Industry-based selection
        if industry in ['technology', 'software', 'ai']:
            return random.choice(['abstract', 'lettermark', 'combination'])
        elif industry in ['consulting', 'finance', 'legal']:
            return random.choice(['wordmark', 'lettermark', 'emblem'])
        elif industry in ['creative', 'design', 'art']:
            return random.choice(['pictorial', 'abstract', 'combination'])
        
        # Name-based selection
        if name_length == 1:
            return random.choice(['lettermark', 'pictorial', 'abstract'])
        elif name_length == 2:
            return random.choice(['combination', 'wordmark'])
        else:
            return 'wordmark'

    def _generate_wordmark(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate a text-focused wordmark logo"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        primary_color = colors[0]
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()
        
        # Calculate text positioning
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1000 - text_width) // 2
        y = (1000 - text_height) // 2
        
        # Draw text with subtle shadow
        draw.text((x+3, y+3), company_name, fill='#cccccc', font=font)
        draw.text((x, y), company_name, fill=primary_color, font=font)
        
        # Add decorative underline
        line_y = y + text_height + 20
        draw.rectangle([x, line_y, x + text_width, line_y + 8], fill=colors[1])
        
        filename = f"wordmark_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

    def _generate_lettermark(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate an initials-based lettermark logo"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Extract initials
        initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
        
        # Create circular background
        center = 500
        radius = 400
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill=colors[0])
        
        # Inner circle for depth
        inner_radius = 350
        draw.ellipse([center-inner_radius, center-inner_radius, 
                     center+inner_radius, center+inner_radius], 
                    fill=colors[1])
        
        # Draw initials
        try:
            font = ImageFont.truetype("arial.ttf", 280)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1000 - text_width) // 2
        y = (1000 - text_height) // 2
        
        draw.text((x, y), initials, fill='white', font=font)
        
        filename = f"lettermark_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

    def _generate_pictorial(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate an icon-based pictorial logo"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Industry-specific icons
        if industry in ['technology', 'software']:
            self._draw_tech_icon(draw, colors)
        elif industry in ['finance', 'consulting']:
            self._draw_finance_icon(draw, colors)
        elif industry in ['creative', 'design']:
            self._draw_creative_icon(draw, colors)
        else:
            self._draw_generic_icon(draw, colors)
        
        # Add company name below
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1000 - text_width) // 2
        y = 800
        
        draw.text((x, y), company_name, fill=colors[0], font=font)
        
        filename = f"pictorial_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

    def _draw_tech_icon(self, draw, colors):
        """Draw a technology-themed icon"""
        center = 500
        # Circuit pattern
        for i in range(3):
            for j in range(3):
                x = 300 + i * 200
                y = 200 + j * 150
                draw.rectangle([x-20, y-20, x+20, y+20], fill=colors[0])
                if i < 2:
                    draw.rectangle([x+20, y-5, x+180, y+5], fill=colors[1])
                if j < 2:
                    draw.rectangle([x-5, y+20, x+5, y+130], fill=colors[1])

    def _draw_finance_icon(self, draw, colors):
        """Draw a finance-themed icon"""
        # Upward trending arrow
        points = [(200, 600), (400, 300), (600, 400), (800, 200)]
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=colors[0], width=20)
        
        # Arrow head
        draw.polygon([(800, 200), (750, 220), (750, 180)], fill=colors[0])

    def _draw_creative_icon(self, draw, colors):
        """Draw a creative-themed icon"""
        # Paintbrush
        center = 500
        handle_points = [(center-50, center+200), (center-30, center+200), 
                        (center-10, center-100), (center+10, center-100)]
        draw.polygon(handle_points, fill=colors[2])
        
        # Brush tip
        tip_points = [(center-10, center-100), (center+10, center-100),
                     (center+30, center-150), (center-30, center-150)]
        draw.polygon(tip_points, fill=colors[0])

    def _draw_generic_icon(self, draw, colors):
        """Draw a generic geometric icon"""
        center = 500
        # Geometric shapes
        draw.polygon([(center, center-200), (center+173, center+100), (center-173, center+100)], 
                    fill=colors[0])
        draw.ellipse([center-100, center-100, center+100, center+100], fill=colors[1])

    def _generate_abstract(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate an abstract geometric logo"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        center = 500
        
        # Abstract geometric pattern
        for i in range(6):
            angle = i * 60
            x1 = center + 200 * math.cos(math.radians(angle))
            y1 = center + 200 * math.sin(math.radians(angle))
            x2 = center + 100 * math.cos(math.radians(angle + 30))
            y2 = center + 100 * math.sin(math.radians(angle + 30))
            
            draw.polygon([(center, center), (x1, y1), (x2, y2)], 
                        fill=colors[i % len(colors)])
        
        # Add company name
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1000 - text_width) // 2
        y = 800
        
        draw.text((x, y), company_name, fill=colors[0], font=font)
        
        filename = f"abstract_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

    def _generate_combination(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate a combination mark (text + symbol)"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Symbol on top
        center_x, symbol_y = 500, 300
        symbol_size = 150
        
        # Create symbol based on industry
        if industry in ['technology', 'software']:
            # Hexagon
            points = []
            for i in range(6):
                angle = i * 60
                x = center_x + symbol_size * math.cos(math.radians(angle))
                y = symbol_y + symbol_size * math.sin(math.radians(angle))
                points.append((x, y))
            draw.polygon(points, fill=colors[0])
        else:
            # Circle
            draw.ellipse([center_x-symbol_size, symbol_y-symbol_size,
                         center_x+symbol_size, symbol_y+symbol_size], fill=colors[0])
        
        # Company name below
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1000 - text_width) // 2
        y = 600
        
        draw.text((x, y), company_name, fill=colors[0], font=font)
        
        filename = f"combination_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

    def _generate_emblem(self, company_name: str, industry: str, color_scheme: str) -> str:
        """Generate an emblem-style logo"""
        img = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(img)
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Outer shield shape
        center = 500
        shield_points = [
            (center, 100), (center+200, 200), (center+200, 600),
            (center, 800), (center-200, 600), (center-200, 200)
        ]
        draw.polygon(shield_points, fill=colors[0])
        
        # Inner border
        inner_points = [
            (center, 150), (center+150, 230), (center+150, 570),
            (center, 750), (center-150, 570), (center-150, 230)
        ]
        draw.polygon(inner_points, fill=colors[1])
        
        # Company initials in center
        initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
        
        try:
            font = ImageFont.truetype("arial.ttf", 150)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1000 - text_width) // 2
        y = (1000 - text_height) // 2
        
        draw.text((x, y), initials, fill='white', font=font)
        
        # Company name banner
        banner_y = 850
        draw.rectangle([200, banner_y-30, 800, banner_y+30], fill=colors[2])
        
        try:
            small_font = ImageFont.truetype("arial.ttf", 40)
        except:
            small_font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), company_name, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (1000 - text_width) // 2
        
        draw.text((x, banner_y-15), company_name, fill='white', font=small_font)
        
        filename = f"emblem_{company_name.replace(' ', '_').lower()}.png"
        filepath = os.path.join('/tmp', filename)
        img.save(filepath)
        return filepath

# Initialize the generator
logo_generator = ProfessionalLogoGenerator()

@app.get("/")
async def root():
    return {
        "message": "AI Logo Generator API",
        "version": "2.0.0",
        "status": "operational",
        "categories": list(logo_generator.categories.keys())
    }

@app.post("/generate-logo")
async def generate_logo(request: LogoRequest):
    """Generate a professional logo"""
    try:
        # Create tmp directory if it doesn't exist
        os.makedirs('/tmp', exist_ok=True)
        
        logo_path = logo_generator.generate_professional_logo(
            company_name=request.company_name,
            industry=request.industry,
            style=request.style,
            color_scheme=request.color_scheme
        )
        
        return {
            "success": True,
            "message": "Professional logo generated successfully",
            "logo_path": logo_path,
            "logo_url": f"/images/{os.path.basename(logo_path)}",  # Add web-accessible URL
            "company_name": request.company_name,
            "industry": request.industry,
            "style": request.style,
            "color_scheme": request.color_scheme
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logo generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Logo Generator"}

@app.get("/images/{filename}")
async def serve_image(filename: str):
    """Serve generated logo images"""
    try:
        file_path = os.path.join('/tmp', filename)
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )