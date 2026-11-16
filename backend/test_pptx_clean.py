import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Slide 1: Title
slide_layout = prs.slide_layouts[0] # standard Title Slide layout
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "ContentIQ"
subtitle.text = "An AI-Powered Multi-Tenant Content Performance and Scheduling Platform\n222301907 Capstone Project – II | GLS University FCAIT\nAcademic Year 2026–2027"

prs.save(r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\test_clean.pptx")
print("Saved clean test pptx")
