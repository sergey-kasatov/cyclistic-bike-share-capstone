import os
from fpdf import FPDF

# Resolve BASE_DIR relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
OUTPUT_PDF = os.path.join(REPORTS_DIR, "cyclistic_case_study_presentation.pdf")

# Image paths
rides_per_day_img = os.path.join(FIGURES_DIR, "rides_per_day.png")
duration_per_day_img = os.path.join(FIGURES_DIR, "duration_per_day.png")
top_start_stations_img = os.path.join(FIGURES_DIR, "top_start_stations.png")
monthly_trends_img = os.path.join(FIGURES_DIR, "monthly_trends.png")

class CyclisticSlides(FPDF):
    def __init__(self):
        super().__init__(orientation="landscape", unit="mm", format="A4")
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(False)
        
    def add_title_slide(self, title, subtitle, author, date):
        self.add_page()
        self.set_fill_color(15, 32, 39)
        self.rect(0, 0, 297, 210, "F")
        self.set_fill_color(255, 127, 14)
        self.rect(0, 0, 8, 210, "F")
        self.set_fill_color(31, 119, 180)
        self.rect(8, 0, 4, 210, "F")
        
        self.set_y(60)
        self.set_x(25)
        self.set_font("Helvetica", "B", 38)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, title, ln=True, align="L")
        
        self.set_x(25)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(200, 214, 224)
        self.cell(0, 10, subtitle, ln=True, align="L")
        
        self.set_draw_color(255, 127, 14)
        self.set_line_width(1)
        self.line(25, 95, 200, 95)
        
        self.set_y(115)
        self.set_x(25)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"Author: {author}", ln=True, align="L")
        
        self.set_x(25)
        self.set_font("Helvetica", "", 12)
        self.set_text_color(170, 185, 195)
        self.cell(0, 6, "Google Data Analytics Professional Certificate Capstone", ln=True, align="L")
        self.set_x(25)
        self.cell(0, 6, f"Date: {date}", ln=True, align="L")
        
        self.set_fill_color(31, 119, 180)
        self.rect(25, 190, 80, 2, "F")

    def draw_slide_header(self, slide_num, title):
        self.add_page()
        self.set_fill_color(245, 247, 250)
        self.rect(0, 0, 297, 210, "F")
        self.set_fill_color(15, 32, 39)
        self.rect(0, 0, 297, 22, "F")
        self.set_fill_color(255, 127, 14)
        self.rect(0, 22, 297, 1.5, "F")
        
        self.set_y(6)
        self.set_x(15)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"Slide {slide_num}: {title}", ln=True, align="L")
        
        self.set_y(201)
        self.set_x(15)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(128, 128, 128)
        self.cell(150, 5, "Cyclistic Bike-Share Case Study", ln=False, align="L")
        self.cell(0, 5, f"Page {slide_num}", ln=False, align="R")

    def add_split_slide(self, slide_num, title, left_bullets, right_content_type, right_data=None):
        self.draw_slide_header(slide_num, title)
        self.set_y(32)
        self.set_text_color(33, 33, 33)
        for bp in left_bullets:
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(255, 127, 14)
            self.cell(5, 6, chr(149), ln=False)
            self.set_text_color(33, 33, 33)
            self.set_font("Helvetica", "", 11)
            self.multi_cell(110, 5.5, bp)
            self.ln(2)
            
        if right_content_type == "image" and right_data:
            img_path = right_data.get("path")
            img_w = right_data.get("w", 145)
            img_h = right_data.get("h", 95)
            img_y = right_data.get("y", 35)
            img_x = 138
            if os.path.exists(img_path):
                self.image(img_path, x=img_x, y=img_y, w=img_w, h=img_h)
                
        elif right_content_type == "stats_card" and right_data:
            card_x = 138
            card_y = 35
            card_w = 144
            card_h = 160
            self.set_fill_color(255, 255, 255)
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.5)
            self.rect(card_x, card_y, card_w, card_h, "FD")
            
            self.set_fill_color(31, 119, 180)
            self.rect(card_x, card_y, card_w, 12, "F")
            self.set_y(card_y + 3)
            self.set_x(card_x)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(255, 255, 255)
            self.cell(card_w, 6, right_data.get("title", "Dataset Overview").upper(), ln=True, align="C")
            
            self.set_text_color(33, 33, 33)
            self.set_y(card_y + 20)
            for item in right_data.get("items", []):
                self.set_x(card_x + 10)
                self.set_font("Helvetica", "B", 12)
                self.cell(0, 6, item[0], ln=True)
                
                self.set_x(card_x + 10)
                self.set_font("Helvetica", "", 11)
                self.set_text_color(100, 100, 100)
                self.multi_cell(card_w - 20, 5, item[1])
                self.set_text_color(33, 33, 33)
                self.ln(4)

    def add_infographic_slide(self, slide_num, title, left_bullets):
        self.draw_slide_header(slide_num, title)
        self.set_y(32)
        self.set_x(15)
        for bp in left_bullets:
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(255, 127, 14)
            self.cell(5, 5.5, chr(149), ln=False)
            self.set_text_color(33, 33, 33)
            self.set_font("Helvetica", "", 10.5)
            self.multi_cell(110, 5, bp)
            self.ln(2.5)
            
        card_w, card_h = 68, 68
        x1, x2 = 138, 214
        y1, y2 = 35, 115
        
        cards_data = [
            {
                "title": "ANNUAL MEMBERS", "val": "64.7%", "sub": "3.73 Million Trips",
                "color": [31, 119, 180], "desc": "Represents the core user base. They ride mostly during weekdays for routine commutes."
            },
            {
                "title": "CASUAL RIDERS", "val": "35.3%", "sub": "2.03 Million Trips",
                "color": [255, 127, 14], "desc": "Key target for conversion. They use bikes heavily for weekend recreation."
            },
            {
                "title": "CASUAL TRIP DURATION", "val": "22.57 min", "sub": "Average Trip Length",
                "color": [255, 127, 14], "desc": "Casual trips are almost 2x longer than members, indicating leisure usage patterns."
            },
            {
                "title": "MEMBER TRIP DURATION", "val": "12.73 min", "sub": "Average Trip Length",
                "color": [31, 119, 180], "desc": "Shorter and more focused trip durations reflect quick utility-driven commutes."
            }
        ]
        
        positions = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        for idx, card in enumerate(cards_data):
            cx, cy = positions[idx]
            self.set_fill_color(255, 255, 255)
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.4)
            self.rect(cx, cy, card_w, card_h, "FD")
            
            self.set_fill_color(*card["color"])
            self.rect(cx, cy, card_w, 4, "F")
            
            self.set_y(cy + 8)
            self.set_x(cx)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(100, 100, 100)
            self.cell(card_w, 4, card["title"].upper(), ln=True, align="C")
            
            self.set_y(cy + 13)
            self.set_x(cx)
            self.set_font("Helvetica", "B", 20)
            self.set_text_color(*card["color"])
            self.cell(card_w, 10, card["val"], ln=True, align="C")
            
            self.set_y(cy + 24)
            self.set_x(cx)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(33, 33, 33)
            self.cell(card_w, 4, card["sub"], ln=True, align="C")
            
            self.set_y(cy + 32)
            self.set_x(cx + 5)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(120, 120, 120)
            self.multi_cell(card_w - 10, 4.2, card["desc"], align="C")

    def add_recommendations_slide(self, slide_num, title):
        self.draw_slide_header(slide_num, title)
        card_w, card_h = 128, 72
        x1, x2 = 15, 154
        y1, y2 = 36, 118
        
        recs = [
            {
                "num": "01",
                "title": "INTRODUCE A WEEKEND-ONLY PASS",
                "color": [255, 127, 14],
                "desc": "Casual riders peak heavily on Saturday and Sunday. Designing a specific weekend-only annual membership will capture these recreational riders who do not need a weekday commute option."
            },
            {
                "num": "02",
                "title": "PROMOTE FINANCIAL SAVINGS",
                "color": [31, 119, 180],
                "desc": "Casual riders average 22.5 minutes per trip (double that of members). Run campaigns proving that purchasing an annual membership saves money compared to buying multiple single-ride passes."
            },
            {
                "num": "03",
                "title": "STATION-SPECIFIC MARKETING",
                "color": [31, 119, 180],
                "desc": "Focus conversion ads, QR code discounts, and physical marketing stands directly around the top 10 casual rider starting stations (e.g., Navy Pier, DuSable Lake Shore Dr, Millennium Park)."
            },
            {
                "num": "04",
                "title": "SUMMER CAMPAIGN WINDOW",
                "color": [255, 127, 14],
                "desc": "Casual rides skyrocket in June, July, and August, dropping to near-zero in winter. Focus the marketing budget heavily during these summer months when engagement and interest are at their peak."
            }
        ]
        
        positions = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        for idx, rec in enumerate(recs):
            cx, cy = positions[idx]
            self.set_fill_color(255, 255, 255)
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.5)
            self.rect(cx, cy, card_w, card_h, "FD")
            
            self.set_fill_color(*rec["color"])
            self.rect(cx, cy, 12, card_h, "F")
            
            self.set_y(cy + 4)
            self.set_x(cx)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(255, 255, 255)
            self.cell(12, 6, rec["num"], ln=False, align="C")
            
            self.set_y(cy + 4)
            self.set_x(cx + 16)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*rec["color"])
            self.cell(card_w - 20, 6, rec["title"], ln=True, align="L")
            
            self.set_draw_color(240, 240, 240)
            self.set_line_width(0.3)
            self.line(cx + 16, cy + 12, cx + card_w - 6, cy + 12)
            
            self.set_y(cy + 15)
            self.set_x(cx + 16)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(100, 100, 100)
            self.multi_cell(card_w - 22, 5.2, rec["desc"], align="L")

    def add_plots_slide(self, slide_num, title, left_bullets, img1_path, img2_path):
        self.draw_slide_header(slide_num, title)
        self.set_y(32)
        self.set_x(15)
        for bp in left_bullets:
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(255, 127, 14)
            self.cell(5, 5.5, chr(149), ln=False)
            self.set_text_color(33, 33, 33)
            self.set_font("Helvetica", "", 11)
            self.multi_cell(110, 5.5, bp)
            self.ln(2.5)
            
        img_w, img_h = 144, 76
        img_x = 138
        y1, y2 = 33, 117
        
        if os.path.exists(img1_path):
            self.image(img1_path, x=img_x, y=y1, w=img_w, h=img_h)
        if os.path.exists(img2_path):
            self.image(img2_path, x=img_x, y=y2, w=img_w, h=img_h)


def main():
    slides = CyclisticSlides()
    slides.add_title_slide(
        title="Cyclistic Bike-Share Case Study",
        subtitle="Analyzing differences in how members and casual riders use Cyclistic bikes",
        author="Sergey Kasatov",
        date="July 2026"
    )
    
    slides.add_split_slide(
        slide_num=2,
        title="The Business Task & Objectives (Ask)",
        left_bullets=[
            "Analyzing historical trip data to understand how annual members and casual riders use Cyclistic bikes differently.",
            "Using these key insights to design a targeted marketing strategy aimed at converting casual riders into annual members.",
            "Key Stakeholder Moreno (Director of Marketing) wants to design digital campaigns to maximize high-margin annual memberships.",
            "Final success requires backing up recommendations with professional data visualizations and clear statistical evidence."
        ],
        right_content_type="stats_card",
        right_data={
            "title": "Key Objectives",
            "items": [
                ["Identify Core Behaviors", "Analyze trip volumes, durations, and weekly patterns to draw distinct profiles of members and casuals."],
                ["Formulate Strategy", "Convert casual riders into annual members by appealing to their specific usage patterns."],
                ["Data-Driven Recommendations", "Backup findings with clear visualizations and statistical metrics for executives."]
            ]
        }
    )
    
    slides.add_split_slide(
        slide_num=3,
        title="Data Prep & Processing (Prepare & Process)",
        left_bullets=[
            "Data Source: Divvy public bike-share historical trip data from July 2025 to June 2026 (12 months).",
            "Initial Dataset: ~5.93 million rows loaded and merged using Python and pandas.",
            "Calculations: Computed ride length (ended_at - started_at) in minutes and extracted day of the week.",
            "Data Cleaning: Excluded trips shorter than 1 minute or with negative durations (docking checks and errors).",
            "Final Cleaned Dataset: 5,770,103 rows utilized for analysis (2.73% of erroneous rows removed)."
        ],
        right_content_type="stats_card",
        right_data={
            "title": "Data Pipeline Summary",
            "items": [
                ["Raw Trips Collected", "5,932,349 rows merged from 12 CSV monthly files."],
                ["Standardized Datetimes", "Parsed started_at and ended_at string columns to datetime objects."],
                ["Calculated Trip Duration", "Derived ride_length in minutes to check trip lengths."],
                ["Filtered Dataset Size", "5,770,103 clean rows kept for analysis (162,246 rows removed)."]
            ]
        }
    )
    
    slides.add_infographic_slide(
        slide_num=4,
        title="Key Insights: Volume & Duration (Analyze)",
        left_bullets=[
            "Annual Members account for 64.7% (3.73M rides) of the total, while Casual Riders represent 35.3% (2.03M rides).",
            "Casual riders travel for an average of 22.57 minutes per trip, whereas Annual Members average 12.73 minutes.",
            "Casual riders ride almost twice as long per trip compared to members, strongly suggesting recreational and leisure usage.",
            "Members' trips are shorter and more uniform, which indicates routine utility-driven trips (commuting to work/school)."
        ]
    )
    
    slides.add_plots_slide(
        slide_num=5,
        title="Weekly Patterns: Rides Count & Trip Duration",
        left_bullets=[
            "Members show high activity on weekdays (Monday to Friday), reflecting commuting behavior.",
            "Casual riders peak heavily on weekends (Saturday and Sunday), reflecting leisure activity.",
            "Casual riders ride significantly longer than members every single day of the week, with durations peaking on weekends."
        ],
        img1_path=rides_per_day_img,
        img2_path=duration_per_day_img
    )
    
    slides.add_split_slide(
        slide_num=6,
        title="Monthly Seasonality Analysis",
        left_bullets=[
            "Both members and casual riders exhibit strong seasonal patterns, with rides peaking in summer (June to August) and dropping in winter.",
            "Casual riders are extremely sensitive to seasons: summer rides are over 10x higher than winter rides.",
            "Members maintain a highly stable base of rides throughout the year (spring and autumn remain solid for work commutes)."
        ],
        right_content_type="image",
        right_data={"path": monthly_trends_img, "w": 144, "h": 78, "y": 32}
    )
    
    slides.add_split_slide(
        slide_num=7,
        title="Top Start Stations for Casual Riders",
        left_bullets=[
            "Casual riders are highly concentrated around waterfront locations, parks, and major tourist hubs.",
            "Navy Pier is the absolute #1 starting location for casual riders with over 45,000 trips.",
            "Other popular stations include DuSable Lake Shore Dr & Monroe St and Michigan Ave & Oak St."
        ],
        right_content_type="image",
        right_data={"path": top_start_stations_img, "w": 144, "h": 85, "y": 32}
    )
    
    slides.add_recommendations_slide(
        slide_num=8,
        title="Strategic Marketing Recommendations (Act)"
    )
    
    slides.add_title_slide(
        title="Thank You!",
        subtitle="Questions & Answers  |  Google Data Analytics Capstone Case Study",
        author="Sergey Kasatov",
        date="July 2026"
    )
    
    slides.output(OUTPUT_PDF)
    print(f"PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == '__main__':
    main()
