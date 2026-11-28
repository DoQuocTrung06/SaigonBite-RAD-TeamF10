using SaigonBite.Domain;

namespace SaigonBite.Controllers
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC14: Manage brands and menu items
    public class BrandCatalogHandler
    {
        private Brand _currentBrand = new();
        private readonly Hub _hubService = new();

        public List<Brand> openBrandCatalog()
        {
            var brands = _currentBrand.getAllBrands();
            var hubs = _hubService.getActiveHubs();
            return brands;
        }

        public Brand selectBrand(string brandId)
        {
            var brand = _currentBrand.getBrandCatalog(brandId)
                ?? new Brand { BrandId = brandId };
            _currentBrand = brand;
            _hubService.getAvailableStations(brandId);
            return _currentBrand;
        }

        public string saveBrandDetails(string brandName, string cuisineType, List<string> assignedHubs)
        {
            string brandId = _currentBrand.saveBrandProfile(brandName, cuisineType, assignedHubs);
            return $"Brand '{brandName}' ({brandId}) assigned to hubs [{string.Join(", ", assignedHubs)}].";
        }

        public string saveMenuItem(string itemCode, string nameVi, string nameEn, decimal unitPrice, string stationType)
        {
            _hubService.verifyStationSupport(stationType);
            return _currentBrand.saveBrandMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType);
        }

        public string discontinueMenuItem(string itemCode)
        {
            return _currentBrand.discontinueBrandItem(itemCode);
        }
    }
}
