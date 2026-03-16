# REAL BOT DETECTOR - reads CSV file!

import csv  # This helps us read CSV files!

def detect_bot_score(visitor):
    bot_score = 0
    
    # Rule 1: Page load time
    if visitor["page_load_time"] < 0.1:
        bot_score += 40
    elif visitor["page_load_time"] < 0.5:
        bot_score += 20
    
    # Rule 2: Time on site
    if visitor["time_on_site"] < 5:
        bot_score += 30
    elif visitor["time_on_site"] < 30:
        bot_score += 15
    
    # Rule 3: Mouse movements
    if visitor["mouse_movements"].lower() == "false":
        bot_score += 30
    
    # Rule 4: Check user agent for bot keywords
    bot_keywords = ["bot", "crawler", "spider", "headless"]
    for keyword in bot_keywords:
        if keyword.lower() in visitor["user_agent"].lower():
            bot_score += 20
    
    return bot_score

# Read the CSV file
visitors_data = []
with open('rvisitors.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert strings to numbers
        row["page_load_time"] = float(row["page_load_time"])
        row["time_on_site"] = float(row["time_on_site"])
        visitors_data.append(row)

# ANALYZE each visitor!
print("="*60)
print("BOT DETECTOR RESULTS ")
print("="*60)

results = []
for visitor in visitors_data:
    score = detect_bot_score(visitor)
    
    if score < 25:
        verdict = " REAL HUMAN"
    elif score < 60:
        verdict = " SUSPICIOUS"
    else:
        verdict = " BOT"
    
    print(f"\n{visitor['name']}")
    print(f"  Bot Score: {score}%")
    print(f"  Verdict: {verdict}")
    print(f"  User Agent: {visitor['user_agent']}")
    
    results.append({
        "name": visitor["name"],
        "score": score,
        "verdict": verdict
    })

# SAVE results to a file!
with open('bot_detection_results.txt', 'w') as file:
    file.write("BOT DETECTION RESULTS\n")
    file.write("="*60 + "\n\n")
    for result in results:
        file.write(f"{result['name']}: {result['score']}% - {result['verdict']}\n")

print("\n" + "="*60)
print(" Results saved to bot_detection_results.txt!")
print("="*60)