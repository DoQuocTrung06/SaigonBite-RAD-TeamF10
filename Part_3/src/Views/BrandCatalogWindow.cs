using SaigonBite.Controllers;

namespace SaigonBite.Views
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class BrandCatalogWindow
    {
        private readonly BrandCatalogHandler _handler;

        public BrandCatalogWindow(BrandCatalogHandler handler)
        {
            _handler = handler;
        }

        public string openBrandCatalog()
        {
            var brands = _handler.openBrandCatalog();
            string msg = $"[BrandCatalogWindow] Loaded {brands.Count} virtual brands and active hub assignments.";
            Console.WriteLine(msg);
            return msg;
        }

        public string selectBrand(string brandId)
        {
            var brand = _handler.selectBrand(brandId);
            string msg = $"[BrandCatalogWindow] Selected brand '{brand.BrandName}' ({brand.BrandId}) with {brand.MenuItems.Count} menu items.";
            Console.WriteLine(msg);
            return msg;
        }

        public string saveBrandDetails(string brandName, string cuisineType, List<string> assignedHubs)
        {
            string msg = _handler.saveBrandDetails(brandName, cuisineType, assignedHubs);
            Console.WriteLine($"[BrandCatalogWindow] {msg}");
            return msg;
        }

        public string saveMenuItem(string itemCode, string nameVi, string nameEn, decimal unitPrice, string stationType)
        {
            string msg = _handler.saveMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType);
            Console.WriteLine($"[BrandCatalogWindow] {msg}");
            return msg;
        }

        public string discontinueMenuItem(string itemCode)
        {
            string msg = _handler.discontinueMenuItem(itemCode);
            Console.WriteLine($"[BrandCatalogWindow] {msg}");
            return msg;
        }
    }
}
