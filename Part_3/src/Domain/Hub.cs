namespace SaigonBite.Domain
{
    public class Hub
    {
        public string HubId { get; set; } = string.Empty;
        public string HubName { get; set; } = string.Empty;
        public int MaxCapacityOrders { get; set; } = 50;
        public int CurrentActiveOrders { get; set; }
        public bool IsBusy { get; set; }

        public bool IsOverloaded()
        {
            if (MaxCapacityOrders <= 0) return true;
            double loadRatio = (double)CurrentActiveOrders / MaxCapacityOrders;
            IsBusy = loadRatio >= 0.85;
            return IsBusy;
        }
    }
}
