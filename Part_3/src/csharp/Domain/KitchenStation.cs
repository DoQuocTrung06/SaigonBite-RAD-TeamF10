namespace SaigonBite.Domain
{
    public class KitchenStation
    {
        public string StationId { get; set; } = string.Empty;
        public string HubId { get; set; } = string.Empty;
        public string StationName { get; set; } = string.Empty;
        public string StationType { get; set; } = "Grill";
        public int CurrentLoadOrders { get; set; }
        public int CapacityLimit { get; set; } = 15;
    }
}
