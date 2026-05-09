from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# AWS Pricing (approximate monthly USD prices as of 2024)
AWS_PRICING = {
    "ec2": {
        "t2.micro":    {"price": 8.47,   "label": "t2.micro (1 vCPU · 1GB RAM)"},
        "t2.small":    {"price": 16.94,  "label": "t2.small (1 vCPU · 2GB RAM)"},
        "t2.medium":   {"price": 33.89,  "label": "t2.medium (2 vCPU · 4GB RAM)"},
        "t3.medium":   {"price": 30.37,  "label": "t3.medium (2 vCPU · 4GB RAM)"},
        "t3.large":    {"price": 60.74,  "label": "t3.large (2 vCPU · 8GB RAM)"},
        "m5.large":    {"price": 70.08,  "label": "m5.large (2 vCPU · 8GB RAM)"},
        "m5.xlarge":   {"price": 140.16, "label": "m5.xlarge (4 vCPU · 16GB RAM)"},
        "m5.2xlarge":  {"price": 280.32, "label": "m5.2xlarge (8 vCPU · 32GB RAM)"},
        "c5.large":    {"price": 62.05,  "label": "c5.large (2 vCPU · 4GB RAM)"},
        "c5.xlarge":   {"price": 124.10, "label": "c5.xlarge (4 vCPU · 8GB RAM)"},
        "r5.large":    {"price": 91.98,  "label": "r5.large (2 vCPU · 16GB RAM)"},
        "r5.xlarge":   {"price": 183.96, "label": "r5.xlarge (4 vCPU · 32GB RAM)"},
    },
    "rds": {
        "db.t3.micro":   {"price": 14.60,  "label": "db.t3.micro (2 vCPU · 1GB)"},
        "db.t3.small":   {"price": 29.20,  "label": "db.t3.small (2 vCPU · 2GB)"},
        "db.t3.medium":  {"price": 58.40,  "label": "db.t3.medium (2 vCPU · 4GB)"},
        "db.m5.large":   {"price": 124.10, "label": "db.m5.large (2 vCPU · 8GB)"},
        "db.m5.xlarge":  {"price": 248.20, "label": "db.m5.xlarge (4 vCPU · 16GB)"},
        "db.r5.large":   {"price": 175.20, "label": "db.r5.large (2 vCPU · 16GB)"},
    },
    "s3": {
        "standard":      {"price": 0.023,  "label": "Standard (per GB)"},
        "infrequent":    {"price": 0.0125, "label": "Infrequent Access (per GB)"},
        "glacier":       {"price": 0.004,  "label": "Glacier (per GB)"},
    },
    "elb": {
        "application":   {"price": 22.27,  "label": "Application Load Balancer"},
        "network":       {"price": 19.71,  "label": "Network Load Balancer"},
        "classic":       {"price": 18.40,  "label": "Classic Load Balancer"},
    },
    "nat": {
        "nat_gateway":   {"price": 32.40,  "label": "NAT Gateway (per AZ)"},
    },
    "cloudfront": {
        "10tb":          {"price": 85.00,  "label": "Up to 10TB/month"},
        "50tb":          {"price": 340.00, "label": "Up to 50TB/month"},
        "100tb":         {"price": 640.00, "label": "Up to 100TB/month"},
    },
    "lambda": {
        "1m_req":        {"price": 0.20,   "label": "1M requests/month"},
        "10m_req":       {"price": 2.00,   "label": "10M requests/month"},
        "100m_req":      {"price": 20.00,  "label": "100M requests/month"},
    },
    "eks": {
        "cluster":       {"price": 72.00,  "label": "EKS Cluster (per cluster)"},
    },
    "ebs": {
        "gp2":           {"price": 0.10,   "label": "GP2 SSD (per GB/month)"},
        "gp3":           {"price": 0.08,   "label": "GP3 SSD (per GB/month)"},
        "io1":           {"price": 0.125,  "label": "IO1 Provisioned (per GB/month)"},
        "st1":           {"price": 0.045,  "label": "ST1 HDD (per GB/month)"},
    }
}

@app.route('/')
def index():
    return render_template('index.html', pricing=AWS_PRICING)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    resources = data.get('resources', [])
    total = 0
    breakdown = []

    for item in resources:
        service   = item.get('service')
        resource  = item.get('resource')
        quantity  = float(item.get('quantity', 1))

        if service in AWS_PRICING and resource in AWS_PRICING[service]:
            unit_price = AWS_PRICING[service][resource]['price']
            label      = AWS_PRICING[service][resource]['label']
            cost       = unit_price * quantity
            total     += cost
            breakdown.append({
                "service":    service.upper(),
                "resource":   label,
                "quantity":   quantity,
                "unit_price": unit_price,
                "cost":       round(cost, 2)
            })

    return jsonify({
        "total":     round(total, 2),
        "breakdown": breakdown,
        "annual":    round(total * 12, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
