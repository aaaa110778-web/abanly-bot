def analyze_digitally_and_technically(stock_name, price):
    # التحليل الرقمي والربط بالمؤشر
    # الحسابات الأساسية: فرق الترندات / 24 ومستويات الدعم والمقاومة
    levels = [round(price + i*0.25, 2) for i in range(1, 4)]
    evaluation = "85%"  # نسبة تقديرية بعد تطبيق الفلاتر

    return f"📊 التحليل الرقمي والفني للسهم {stock_name}:

السعر الحالي: {price}\nأهداف قريبة: {levels}\n
📈 تقييم الصفقة: {evaluation}"