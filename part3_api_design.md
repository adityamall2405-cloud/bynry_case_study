1. Assumptions
Recent sales = last 30 days
Threshold stored in product table (reorder_threshold)
days_until_stockout =
current_stock / avg_daily_sales

2. Edge Cases Handled
No sales → ignored
Division by zero avoided
Missing supplier handled
Multi-warehouse supported
Empty result safe

3. Approach Explanation
Fetch all inventory per company
Filter by recent sales
Compute:
avg daily sales
days until stockout
Compare against threshold
Attach supplier info