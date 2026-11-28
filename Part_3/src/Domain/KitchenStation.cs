namespace SaigonBite.Domain
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class KitchenStation
    {
        private static readonly HashSet<string> SupportedTypes = new(StringComparer.OrdinalIgnoreCase)
        {
            "Wok", "Fryer", "Assembly", "Beverage", "Grill", "Drink_Dessert"
        };

        public string StationId { get; set; } = string.Empty;
        public string HubId { get; set; } = string.Empty;
        public string StationName { get; set; } = string.Empty;
        public string StationType { get; set; } = "Wok";
        public int CurrentLoadOrders { get; set; }
        public int CapacityLimit { get; set; } = 15;

        public bool checkStationType(string stationType)
        {
            return SupportedTypes.Contains(stationType)
                && StationType.Equals(stationType, StringComparison.OrdinalIgnoreCase);
        }
    }
}
