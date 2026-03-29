"""
Skill2Job — Razorpay Auto-Injector
====================================
Yeh script automatically Razorpay Checkout JS inject karti hai
teeno HTML files mein.

INSTRUCTIONS:
1. Apni Razorpay Test Key ID neeche daalo (RAZORPAY_KEY_ID)
2. Script run karo: python razorpay_inject.py
3. Files update ho jayengi automatically
4. GitHub push karo — done!
"""

import os
import re

# ─────────────────────────────────────────────
# ✏️  SIRF YAHAN APNI KEY DAALO
RAZORPAY_KEY_ID = "rzp_test_XXXXXXXXXXXXXXrzp_live_SVv0ymYh6gFP1k"  # 👈 Replace with your key
RAZORPAY_AMOUNT = 79900                          # 799 × 100 paise
RAZORPAY_CURRENCY = "INR"
RAZORPAY_BUSINESS_NAME = "Skill2Job"
RAZORPAY_DESCRIPTION = "Excel Job Ready Course"
RAZORPAY_BRAND_COLOR = "#6366f1"
RAZORPAY_LOGO_URL = "https://skill2jobai.com/logo.png"
STUDENT_PORTAL_URL = "/student-portal.html"
# ─────────────────────────────────────────────

REPO_PATH = r"D:\10. Website_Skill2JobAI\1. Github\nrjshrm18-cmyk.github.io"

TARGET_FILES = [
    "index.html",                          # skill2job-homepage
    "excel-job-ready/index.html",          # excel course landing page
    "student-login/index.html",            # student portal
]

RAZORPAY_SCRIPT_TAG = '<script src="https://checkout.razorpay.com/v1/checkout.js"></script>'

RAZORPAY_FUNCTION = f"""
<!-- ✅ Razorpay Integration — Auto-injected by razorpay_inject.py -->
<script>
function openRazorpay() {{
  var options = {{
    key: "{RAZORPAY_KEY_ID}",
    amount: {RAZORPAY_AMOUNT},
    currency: "{RAZORPAY_CURRENCY}",
    name: "{RAZORPAY_BUSINESS_NAME}",
    description: "{RAZORPAY_DESCRIPTION}",
    image: "{RAZORPAY_LOGO_URL}",
    handler: function (response) {{
      alert("✅ Payment Successful!\\nPayment ID: " + response.razorpay_payment_id);
      window.location.href = "{STUDENT_PORTAL_URL}";
    }},
    prefill: {{
      name: "",
      email: "",
      contact: ""
    }},
    theme: {{
      color: "{RAZORPAY_BRAND_COLOR}"
    }}
  }};
  var rzp = new Razorpay(options);
  rzp.open();
}}
</script>
<!-- ✅ End Razorpay Integration -->
"""

def already_injected(content):
    return "checkout.razorpay.com" in content

def inject_script_tag(content):
    """Add Razorpay CDN script before </head>"""
    if RAZORPAY_SCRIPT_TAG in content:
        return content, False
    updated = content.replace("</head>", f"  {RAZORPAY_SCRIPT_TAG}\n</head>", 1)
    return updated, updated != content

def inject_function(content):
    """Add openRazorpay() function before </body>"""
    if "function openRazorpay()" in content:
        return content, False
    updated = content.replace("</body>", f"{RAZORPAY_FUNCTION}\n</body>", 1)
    return updated, updated != content

def update_enroll_buttons(content):
    """
    Find buttons/links with common enroll patterns and add onclick="openRazorpay()"
    Skips buttons that already have openRazorpay
    """
    # Common patterns in Skill2Job files
    patterns = [
        # Buttons with enroll-related text
        r'(<button)([^>]*?)(>(?:Enroll Now|Enroll|Buy Now|Get Started|Purchase|Enroll Now.*?₹\d+)[^<]*?</button>)',
        # Anchor tags acting as buttons with enroll text  
        r'(<a)([^>]*?)(>(?:Enroll Now|Enroll|Buy Now|Get Started|Purchase)[^<]*?</a>)',
    ]
    
    modified = False
    for pattern in patterns:
        def add_onclick(m):
            tag_open = m.group(1)
            attrs = m.group(2)
            rest = m.group(3)
            if "openRazorpay" in attrs:
                return m.group(0)  # already has it
            return f'{tag_open}{attrs} onclick="openRazorpay()"{rest}'
        
        new_content = re.sub(pattern, add_onclick, content, flags=re.IGNORECASE | re.DOTALL)
        if new_content != content:
            content = new_content
            modified = True
    
    return content, modified

def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"  ⚠️  File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    if already_injected(original):
        print(f"  ✅ Already injected, skipping: {filepath}")
        return

    content = original
    changes = []

    content, changed = inject_script_tag(content)
    if changed:
        changes.append("Razorpay CDN script added in <head>")

    content, changed = inject_function(content)
    if changed:
        changes.append("openRazorpay() function added before </body>")

    content, changed = update_enroll_buttons(content)
    if changed:
        changes.append("Enroll buttons updated with onclick handler")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Updated: {filepath}")
        for c in changes:
            print(f"     → {c}")
    else:
        print(f"  ℹ️  No changes needed: {filepath}")

def main():
    print("=" * 55)
    print("  Skill2Job — Razorpay Auto-Injector")
    print("=" * 55)
    print(f"  Repo path : {REPO_PATH}")
    print(f"  Key ID    : {RAZORPAY_KEY_ID[:12]}...")
    print(f"  Amount    : ₹{RAZORPAY_AMOUNT // 100}")
    print("=" * 55)

    if not os.path.exists(REPO_PATH):
        print(f"\n❌ ERROR: Repo path not found!\n   {REPO_PATH}")
        print("   Path check karo aur REPO_PATH update karo script mein.")
        return

    print()
    for filename in TARGET_FILES:
        filepath = os.path.join(REPO_PATH, filename)
        print(f"📄 Processing: {filename}")
        process_file(filepath)
        print()

    print("=" * 55)
    print("  ✅ Done! Ab GitHub push karo:")
    print()
    print("  cd \"" + REPO_PATH + "\"")
    print("  git add .")
    print('  git commit -m "Add Razorpay payment integration"')
    print("  git push")
    print("=" * 55)

if __name__ == "__main__":
    main()
