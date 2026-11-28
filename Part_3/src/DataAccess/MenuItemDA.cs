using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class MenuItemDA
    {
        public static MenuItemDA Instance { get; } = new();
        private readonly Dictionary<string, MenuItem> _items = new(StringComparer.OrdinalIgnoreCase);

        public List<MenuItem> readMenuItemsByBrand(string brandId)
        {
            const string sql = @"
                SELECT item_id, brand_id, item_name_vi, item_name_en, description, unit_price, station_type, status
                FROM menu_items WHERE brand_id = @brandId ORDER BY item_id;";
            _ = sql;
            return _items.Values
                .Where(m => m.BrandId.Equals(brandId, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }

        public bool saveMenuItem(string brandId, MenuItem item)
        {
            const string sql = @"
                INSERT INTO menu_items (item_id, brand_id, item_name_vi, item_name_en, description, unit_price, station_type, status)
                VALUES (@itemId, @brandId, @nameVi, @nameEn, @description, @unitPrice, @stationType, 'Active')
                ON CONFLICT (item_id) DO UPDATE
                SET item_name_vi = EXCLUDED.item_name_vi, item_name_en = EXCLUDED.item_name_en,
                    unit_price = EXCLUDED.unit_price, station_type = EXCLUDED.station_type, status = EXCLUDED.status;";
            _ = sql;
            item.BrandId = brandId;
            _items[item.ItemId] = item;
            return true;
        }

        public bool updateMenuItemStatus(string itemCode, string status)
        {
            const string sql = "UPDATE menu_items SET status = @status WHERE item_id = @itemId;";
            _ = sql;
            if (!_items.TryGetValue(itemCode, out var item))
                return false;
            item.Status = status;
            return true;
        }

        public MenuItem? FindByCode(string itemCode)
        {
            _items.TryGetValue(itemCode, out var item);
            return item;
        }
    }
}
