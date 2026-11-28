namespace SaigonBite.Domain
{
    public class ManagementReport
    {
        public string ReportId { get; set; } = string.Empty;
        public string HubId { get; set; } = string.Empty;
        public string ReportType { get; set; } = "Monthly_Revenue_And_Delivery_Performance";
        public DateTime GeneratedDate { get; set; } = DateTime.UtcNow;
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public decimal TotalRevenue { get; set; }
        public int TotalOrders { get; set; }
        public decimal AvgDeliveryMinutes { get; set; } = 24.5m;
        public decimal WasteCost { get; set; } = 0.0m;

        public void CalculateKPIs(IEnumerable<Order> orders, IEnumerable<DeliveryTask> tasks)
        {
            TotalOrders = orders.Count();
            TotalRevenue = orders.Where(o => o.OrderStatus == "Delivered").Sum(o => o.FinalTotal);
        }
    }
}
