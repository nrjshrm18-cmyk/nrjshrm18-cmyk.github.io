import re, glob

# Sirf enroll/join wale WhatsApp buttons fix karo
# Support/Community wale links touch nahi honge

patterns_to_fix = [
    # mob-sticky-wa button (homepage)
    (r'class="mob-sticky-wa"[^>]*onclick="[^"]*wa\.me[^"]*"', 
     'class="mob-sticky-wa" onclick="openRazorpay()"'),
    
    # wa-btn class (excel landing page)
    (r'class="wa-btn"[^>]*onclick="[^"]*wa\.me[^"]*"',
     'class="wa-btn" onclick="openRazorpay()"'),
    
    # TaskFlow beta join - window.open wa.me (products launcher)
    (r'onclick="closeProductsLauncher\(\);window\.open\(\'https://wa\.me[^\']*\'[^)]*\)"',
     'onclick="closeProductsLauncher();openRazorpay()"'),
]

files = glob.glob('**/*.html', recursive=True)
for f in files:
    content = open(f, encoding='utf-8').read()
    new = content
    for pattern, replacement in patterns_to_fix:
        new = re.sub(pattern, replacement, new, flags=re.IGNORECASE)
    
    if new != content:
        open(f, 'w', encoding='utf-8').write(new)
        print(f"Fixed: {f}")
    else:
        print(f"No change: {f}")

print("\nDone!")
