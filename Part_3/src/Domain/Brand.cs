using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class Brand
    {
        public string BrandId { get; set; } = string.Empty;
        public string BrandName { get; set; } = string.Empty;
        public string CuisineType { get; set; } = string.Empty;
        public string Status { get; set; } = "Active";
        public List<string> AssignedHubIds { get; set; } = new();
        public List<MenuItem> MenuItems { get; set; } = new();

        public List<Brand> getAllBrands()
        {
            return BrandDA.Instance.readAllBrands();
        }

        public Brand? getBrandCatalog(string brandId)
        {
            var brand = BrandDA.Instance.readBrand(brandId);
            if (brand != null)
            {
                brand.MenuItems = new MenuItem().getBrandMenuItems(brandId);
            }
            return brand;
        }

        public string saveBrandProfile(string brandName, string cuisineType, List<string> assignedHubs)
        {
            if (string.IsNullOrWhiteSpace(brandName))
                throw new ArgumentException("Brand name is required.");
            if (assignedHubs == null || assignedHubs.Count == 0)
                throw new ArgumentException("3.1b Missing hub assignment: At least one operational hub must be assigned.");

            var existing = BrandDA.Instance.readAllBrands()
                .FirstOrDefault(b => b.BrandName.Equals(brandName, StringComparison.OrdinalIgnoreCase) && b.BrandId != BrandId);
            if (existing != null)
                throw new InvalidOperationException($"3.1a Duplicate brand identifier: Brand '{brandName}' already exists.");

            if (string.IsNullOrWhiteSpace(BrandId))
                BrandId = $"BR-{BrandDA.Instance.readAllBrands().Count + 1:00}";

            BrandName = brandName;
            CuisineType = cuisineType;
            Status = "Active";
            AssignedHubIds = new List<string>(assignedHubs);

            return BrandDA.Instance.saveBrand(this, assignedHubs);
        }

        public string saveBrandMenuItem(string itemCode, string nameVi, string nameEn, decimal unitPrice, string stationType)
        {
            var item = new MenuItem { BrandId = BrandId };
            var saved = item.publishMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType);
            return $"MenuItem '{saved.ItemId}' ({saved.ItemNameVi} / {saved.ItemNameEn}) saved in state {saved.Status}.";
        }

        public string discontinueBrandItem(string itemCode)
        {
            var item = new MenuItem { BrandId = BrandId };
            bool updated = item.discontinueItem(itemCode);
            if (!updated)
                throw new InvalidOperationException($"MenuItem '{itemCode}' not found.");
            return $"MenuItem '{itemCode}' transitioned to state Discontinued.";
        }
    }
}
