using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class BrandDA
    {
        public static BrandDA Instance { get; } = new();
        private readonly Dictionary<string, Brand> _brands = new(StringComparer.OrdinalIgnoreCase);

        public List<Brand> readAllBrands()
        {
            const string sql = "SELECT brand_id, brand_name, cuisine_type, status FROM brands ORDER BY brand_id;";
            _ = sql;
            return _brands.Values.ToList();
        }

        public Brand? readBrand(string brandId)
        {
            const string sql = "SELECT brand_id, brand_name, cuisine_type, status FROM brands WHERE brand_id = @brandId;";
            _ = sql;
            _brands.TryGetValue(brandId, out var brand);
            return brand;
        }

        public string saveBrand(Brand brand, List<string> assignedHubs)
        {
            const string sqlUpsertBrand = @"
                INSERT INTO brands (brand_id, brand_name, cuisine_type, status)
                VALUES (@brandId, @brandName, @cuisineType, @status)
                ON CONFLICT (brand_id) DO UPDATE
                SET brand_name = EXCLUDED.brand_name, cuisine_type = EXCLUDED.cuisine_type, status = EXCLUDED.status;";
            const string sqlAssignHub = "INSERT INTO brand_hubs (brand_id, hub_id) VALUES (@brandId, @hubId);";
            _ = (sqlUpsertBrand, sqlAssignHub);

            brand.AssignedHubIds = new List<string>(assignedHubs);
            _brands[brand.BrandId] = brand;
            HubDA.Instance.AssignBrandHubs(brand.BrandId, assignedHubs);
            return brand.BrandId;
        }
    }
}
