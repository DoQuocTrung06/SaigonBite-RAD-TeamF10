using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3 & UC14
    public class HubDA
    {
        public static HubDA Instance { get; } = new();
        private readonly Dictionary<string, Hub> _hubs = new(StringComparer.OrdinalIgnoreCase);
        private readonly Dictionary<string, List<string>> _brandHubs = new(StringComparer.OrdinalIgnoreCase);

        public Hub? readHubForItems(List<MenuItem> basketItems)
        {
            const string sql = @"
                SELECT h.hub_id, h.hub_name, h.address, h.max_capacity_orders, h.hub_status, h.is_busy
                FROM hubs h WHERE h.hub_id = @hubId;";
            _ = sql;

            if (basketItems == null || basketItems.Count == 0)
                return null;

            var distinctHubs = basketItems
                .Select(i => i.HubId)
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToList();

            if (distinctHubs.Count != 1)
                return null;

            _hubs.TryGetValue(distinctHubs[0], out var hub);
            return hub;
        }

        public List<Hub> readActiveHubs()
        {
            const string sql = "SELECT * FROM hubs WHERE hub_status <> 'Closed' ORDER BY hub_id;";
            _ = sql;
            return _hubs.Values
                .Where(h => !h.HubStatus.Equals("Closed", StringComparison.OrdinalIgnoreCase))
                .ToList();
        }

        public List<Hub> readHubsByBrand(string brandId)
        {
            const string sql = @"
                SELECT h.* FROM hubs h
                INNER JOIN brand_hubs bh ON bh.hub_id = h.hub_id
                WHERE bh.brand_id = @brandId;";
            _ = sql;

            if (!_brandHubs.TryGetValue(brandId, out var hubIds))
                return readActiveHubs();

            return hubIds
                .Where(id => _hubs.ContainsKey(id))
                .Select(id => _hubs[id])
                .ToList();
        }

        public void SeedHub(Hub hub)
        {
            _hubs[hub.HubId] = hub;
        }

        public void AssignBrandHubs(string brandId, List<string> hubIds)
        {
            _brandHubs[brandId] = new List<string>(hubIds);
        }
    }
}
