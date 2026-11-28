namespace SaigonBite.Domain
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class OrderLine
    {
        public string OrderLineId { get; set; } = string.Empty;
        public string ItemId { get; set; } = string.Empty;
        public int Quantity { get; set; }
        public decimal ItemPrice { get; set; }
        public decimal LineTotal { get; set; }
        public string SpecialNotes { get; set; } = string.Empty;
        public string StationType { get; set; } = "Wok";

        public decimal calculateLineTotal(MenuItem item, int qty)
        {
            if (item == null || !item.checkAvailability())
                throw new InvalidOperationException($"Menu item '{item?.ItemId}' is not in state Active.");
            if (qty <= 0)
                throw new ArgumentException("Quantity must be positive.");

            ItemId = item.ItemId;
            Quantity = qty;
            ItemPrice = item.UnitPrice;
            StationType = item.StationType;
            LineTotal = ItemPrice * Quantity;
            return LineTotal;
        }
    }
}
