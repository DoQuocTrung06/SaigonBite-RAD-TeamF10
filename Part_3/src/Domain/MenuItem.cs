using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14 & UC3
    public class MenuItem
    {
        public string ItemId { get; set; } = string.Empty;
        public string BrandId { get; set; } = string.Empty;
        public string HubId { get; set; } = "H01";
        public string ItemNameVi { get; set; } = string.Empty;
        public string ItemNameEn { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public decimal UnitPrice { get; set; }
        public string StationType { get; set; } = "Wok";
        public string Status { get; set; } = "Active"; // Active, Suspended, Discontinued

        public List<MenuItem> getBrandMenuItems(string brandId)
        {
            return MenuItemDA.Instance.readMenuItemsByBrand(brandId);
        }

        public MenuItem publishMenuItem(string itemCode, string nameVi, string nameEn, decimal unitPrice, string stationType)
        {
            if (string.IsNullOrWhiteSpace(itemCode))
                throw new ArgumentException("Item code is required.");
            if (unitPrice <= 0)
                throw new ArgumentException("4.1b Invalid unit price (<= 0 VND): Unit price must be greater than 0 VND.");

            var duplicate = MenuItemDA.Instance.FindByCode(itemCode);
            if (duplicate != null && duplicate.BrandId != BrandId)
                throw new InvalidOperationException($"4.1a Duplicate item code: '{itemCode}' already exists.");

            ItemId = itemCode;
            ItemNameVi = nameVi;
            ItemNameEn = nameEn;
            UnitPrice = unitPrice;
            StationType = stationType;
            Status = "Active";

            MenuItemDA.Instance.saveMenuItem(BrandId, this);
            return this;
        }

        public bool discontinueItem(string itemCode)
        {
            Status = "Discontinued";
            return MenuItemDA.Instance.updateMenuItemStatus(itemCode, "Discontinued");
        }

        public bool checkAvailability()
        {
            return Status.Equals("Active", StringComparison.OrdinalIgnoreCase);
        }
    }
}
