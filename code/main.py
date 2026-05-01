import csv

# File names (keep CSV in same folder when running)
INPUT_FILE = "support_issues.csv"
OUTPUT_FILE = "output.csv"


def classify_issue(issue, subject, company):
    text = (issue + " " + subject).lower()

    # Default values
    response = "Please contact support for assistance."
    product_area = "technical"
    status = "replied"
    request_type = "product_issue"
    justification = "General issue"

    # Billing / payment issues
    if any(word in text for word in ["payment", "refund", "charge", "card"]):
        product_area = "billing"
        status = "escalated"
        justification = "Payment-related issue requires secure handling"
        response = "Please contact support or your bank for payment-related assistance."

    # Account / access issues
    elif any(word in text for word in ["access", "login", "account"]):
        product_area = "account_access"
        justification = "Account-related issue"
        response = "Please check your account access or contact your administrator."

    # Technical issues
    elif any(word in text for word in ["error", "not working", "failed", "issue"]):
        product_area = "technical"
        request_type = "bug"
        status = "escalated"
        justification = "Technical issue may require investigation"
        response = "This seems like a technical issue. Please contact support."

    # Fraud / sensitive
    elif "stolen" in text or "fraud" in text:
        product_area = "fraud"
        status = "escalated"
        justification = "Sensitive issue"
        response = "Please contact support immediately to secure your account."

    # Harmful / invalid
    elif "delete all files" in text:
        product_area = "security"
        status = "escalated"
        request_type = "invalid"
        justification = "Unsafe request"
        response = "I cannot assist with harmful actions."

    return response, product_area, status, request_type, justification


def main():
    with open(INPUT_FILE, newline='', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)

        fieldnames = [
            "issue", "subject", "company",
            "response", "product_area",
            "status", "request_type", "justification"
        ]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            issue = row["Issue"]
            subject = row["Subject"]
            company = row["Company"]

            response, product_area, status, request_type, justification = classify_issue(
                issue, subject, company
            )

            writer.writerow({
                "issue": issue,
                "subject": subject,
                "company": company,
                "response": response,
                "product_area": product_area,
                "status": status,
                "request_type": request_type,
                "justification": justification
            })

    print("Output generated successfully!")


if __name__ == "__main__":
    main()
