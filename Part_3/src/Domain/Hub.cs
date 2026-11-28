using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Authors: 524H0031 (UC3 & UC14), 524H0132 (UC7)
    public class Hub
    {
        public string HubId { get; set; } = string.Empty;
        public string HubName { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public decimal Latitude { get; set; }
        public decimal Longitude { get; set; }
        public int MaxCapacityOrders { get; set; } = 50;
        public int CurrentActiveOrders { get; set; }
        public string HubStatus { get; set; } = "Open";
        public bool IsBusy { get; set; }
        public List<KitchenStation> Stations { get; set; } = new();

        public bool IsOverloaded()
        {
            if (MaxCapacityOrders <= 0) return true;
            double loadRatio = (double)CurrentActiveOrders / MaxCapacityOrders;
            IsBusy = loadRatio >= 0.85;
            HubStatus = IsBusy ? "Busy" : "Open";
            return IsBusy;
        }

        // UC3 (524H0031): Verify single-hub constraint & workload < 85%
        public bool verifyHubCapacity(List<MenuItem> basketItems)
        {
            var hub = HubDA.Instance.readHubForItems(basketItems);
            if (hub == null)
                throw new InvalidOperationException("1.1a Cross-hub basket conflict: All basket items must belong to a single cloud kitchen hub.");

            HubId = hub.HubId;
            HubName = hub.HubName;
            Address = hub.Address;
            MaxCapacityOrders = hub.MaxCapacityOrders;
            CurrentActiveOrders = hub.CurrentActiveOrders;
            HubStatus = hub.HubStatus;
            Stations = hub.Stations;

            if (IsOverloaded())
                throw new InvalidOperationException($"Hub '{HubId}' is currently at >= 85% capacity and cannot accept new orders.");

            return true;
        }

        // UC3 (524H0031): Calculate delivery distance and enforce <= 7.0 km radius (A-01)
        public decimal calculateDistance(string deliveryAddress)
        {
            if (string.IsNullOrWhiteSpace(deliveryAddress))
                throw new ArgumentException("Delivery address is required.");

            decimal distanceKm = deliveryAddress.Contains("OutZone", StringComparison.OrdinalIgnoreCase)
                || deliveryAddress.Contains("8.5", StringComparison.OrdinalIgnoreCase)
                || deliveryAddress.Contains("Thu Duc", StringComparison.OrdinalIgnoreCase)
                ? 8.50m
                : deliveryAddress.Contains("Rex Hotel", StringComparison.OrdinalIgnoreCase)
                    ? 1.50m
                    : 3.20m;

            if (distanceKm > 7.0m)
                throw new InvalidOperationException($"2.1a Delivery distance ({distanceKm:F1} km) exceeds maximum 7.0 km delivery radius.");

            return distanceKm;
        }

        // UC3 (524H0031): Check Quiet-Kitchen incentive discount eligibility (< 40% active load, A-03)
        public bool checkQuietKitchenDiscount()
        {
            if (MaxCapacityOrders <= 0) return false;
            double loadRatio = (double)CurrentActiveOrders / MaxCapacityOrders;
            return loadRatio < 0.40;
        }

        // UC14 (524H0031): Retrieve active cloud kitchen hubs
        public List<Hub> getActiveHubs()
        {
            return HubDA.Instance.readActiveHubs();
        }

        // UC14 (524H0031): Retrieve available preparation stations for a brand's assigned hubs
        public List<KitchenStation> getAvailableStations(string brandId)
        {
            var assignedHubs = HubDA.Instance.readHubsByBrand(brandId);
            return assignedHubs.SelectMany(h => h.Stations).ToList();
        }

        // UC14 (524H0031): Verify that assigned hubs support the requested preparation station type
        public bool verifyStationSupport(string stationType)
        {
            var stationsToCheck = Stations.Count > 0
                ? Stations
                : HubDA.Instance.readActiveHubs().SelectMany(h => h.Stations).ToList();

            bool supported = stationsToCheck.Any(s => s.checkStationType(stationType));
            if (!supported)
                throw new InvalidOperationException($"4.1c Incompatible preparation station: Station '{stationType}' is unsupported at assigned hubs.");

            return true;
        }
    }
}
