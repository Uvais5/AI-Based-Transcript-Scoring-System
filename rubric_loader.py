import pandas as pd

def load_rubric(file_path):
    """
    Loads the rubric from the Excel file.
    Returns a structured dictionary or list of criteria.
    """
    try:
        # Load the specific sheet
        df = pd.read_excel(file_path, sheet_name='Rubrics', header=None)
        
        rubric = []
        current_category = "General"
        
        # Iterate through rows starting from where data likely begins (Row 14 in analysis, index 14)
        # Based on analysis:
        # Col 1 (index 1): Category? Or Col 0?
        # Analysis shows:
        # 14: NaN, Content & Structure, Salutation Level, 5, 40
        # Let's assume:
        # Col 1: Category
        # Col 2: Criteria Name / Description
        # Col 3: Metric / Target
        # Col 4: Weightage
        
        # Adjusting based on the visual output in analysis_output.txt
        # Row 14: NaN, Content & Structure, Salutation Level, 5, 40
        # Wait, "Salutation Level" is in Col 3? "Content & Structure" in Col 1?
        # Let's look at the analysis again.
        # 87: 14 NaN Content & Structure Salutation Level 5 40
        # Col 0: NaN
        # Col 1: Content & Structure
        # Col 2: Salutation Level
        # Col 3: 5 (Metric?)
        # Col 4: 40 (Weight?)
        
        # Row 15: NaN, NaN, Key word Presence..., 30
        # Col 4 seems to be Weight for Row 14? Or is it 40?
        # Row 17: Speech Rate, Speech rate..., 10, 10
        
        # Let's try to be dynamic.
        # We will look for rows where we have a weight.
        
        start_row = 14 # Based on analysis
        
        for index, row in df.iterrows():
            if index < start_row:
                continue
                
            # Check if it's a valid row with weight
            # Assuming Weight is in column 4 (index 4) or 3?
            # Row 14: 5, 40. Maybe 5 is metric, 40 is weight?
            # Row 17: 10, 10.
            # Row 18: 10, 20.
            
            # Let's assume the last non-NaN numeric value is weight, or specifically Col 4.
            # Let's look at Row 14 again: "Salutation Level", 5, 40. 
            # 5 might be "Max Score" or "Target"? 40 is likely weight if total is 100.
            # 40 + 30 + 5 + 10 + 20 + ? 
            # 40+30+5 = 75. 10+20 = 30. Total > 100?
            # Let's re-read the analysis carefully.
            # Row 14: Salutation Level, 5, 40
            # Row 15: Keyword Presence, 30. (Col 3 or 4?)
            # Row 16: Flow, 5.
            # Row 17: Speech Rate, 10, 10.
            # Row 18: Grammar, 10, 20.
            # Row 19: Vocab, 10.
            
            # 40+30+5 = 75.
            # 10+20+10 = 40.
            # Total = 115?
            # Maybe Col 3 is Weight?
            # Row 14: 5. Row 15: 30. Row 16: 5. Row 17: 10. Row 18: 10. Row 19: 10.
            # 5+30+5+10+10+10 = 70.
            
            # Let's look at Row 14 again.
            # Col 1: Content & Structure
            # Col 2: Salutation Level
            # Col 3: 5
            # Col 4: 40
            
            # Maybe Col 4 is the weight for the *Category*?
            # Content & Structure: 40?
            # But inside: Salutation(5) + Keyword(30) + Flow(5) = 40. Yes!
            # So Col 3 is the weight for the specific criterion.
            
            category_val = row[1]
            if pd.notna(category_val):
                current_category = category_val.strip()
            
            criteria_name = row[2]
            weight = row[3]
            
            if pd.notna(criteria_name) and pd.notna(weight):
                try:
                    weight = float(weight)
                except:
                    continue
                    
                rubric.append({
                    "category": current_category,
                    "criteria": criteria_name.strip(),
                    "weight": weight
                })
                
        return rubric

    except Exception as e:
        print(f"Error loading rubric: {e}")
        return []

if __name__ == "__main__":
    # Test
    r = load_rubric("Case study for interns.xlsx")
    print(r)
