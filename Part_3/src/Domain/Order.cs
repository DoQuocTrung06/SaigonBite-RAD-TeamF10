using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Authors: 524H0031 (UC3), 524H0132 (UC7), 524H0136 (UC10)
    public class Order
    {
        public string OrderId { get; set; } = string.Empty;
        public string CustomerId { get; set; } = "CUS-01";
        public string HubId { get; set; } = "H01";
        public DateTime OrderDateTime { get; set; } = DateTime.UtcNow;
        public DateTime OrderTime
        {
            get => OrderDateTime;
            set => OrderDateTime = value;
        }
        public string OrderStatus { get; set; } = "Placed";
        public string DeliveryAddress { get; set; } = string.Empty;
        public decimal DistanceKm { get; set; }
        public decimal Subtotal { get; set; }
        public decimal DeliveryFee { get; set; }
        public decimal DiscountAmount { get; set; }
        public decimal QuietDiscountAmount { get; set; }
        public decimal VoucherDiscountAmount { get; set; }
        public decimal FinalTotal { get; set; }
        public string PaymentMethod { get; set; } = "Cash on Delivery";
        public string? AppliedVoucherCode { get; set; }
        public string? AuthorizationCode { get; set; }
        public DateTime? DeliveredAt { get; set; }
        public string? CancellationReason { get; set; }
        public bool IsLocked { get; set; }
        public List<OrderLine> Lines { get; set; } = new();
        public List<KitchenTicket> Tickets { get; set; } = new();
        public Payment? OrderPayment { get; set; }

        // UC3 (524H0031): Add individual dish line and compute line total
        public OrderLine addOrderLine(MenuItem item, int qty, string notes)
        {
            var line = new OrderLine
            {
                OrderLineId = $"OL-{Lines.Count + 1:000}",
                SpecialNotes = notes
            };
            line.calculateLineTotal(item, qty);
            Lines.Add(line);
            HubId = item.HubId;
            return line;
        }

        // UC3 (524H0031): Sum line totals
        public decimal calculateSubtotal()
        {
            Subtotal = Lines.Sum(l => l.LineTotal);
            FinalTotal = Subtotal + DeliveryFee - DiscountAmount;
            return Subtotal;
        }

        // UC3 (524H0031): Compute distance fee (15,000 VND first 2km + 5,000 VND/extra km) & 10% Quiet-Kitchen discount
        public decimal calculateDeliveryAndTotal(string address, decimal distanceKm, bool quietEligible)
        {
            DeliveryAddress = address;
            DistanceKm = distanceKm;

            decimal extraKm = distanceKm > 2.0m ? Math.Ceiling(distanceKm - 2.0m) : 0m;
            DeliveryFee = 15000m + (extraKm * 5000m);

            QuietDiscountAmount = quietEligible ? Math.Round(Subtotal * 0.10m, 0) : 0m;
            DiscountAmount = QuietDiscountAmount + VoucherDiscountAmount;
            FinalTotal = Math.Max(0m, Subtotal + DeliveryFee - DiscountAmount);
            return FinalTotal;
        }

        // UC3 (524H0031): Validate and apply at most one promotional voucher
        public decimal applyVoucherDiscount(string voucherCode)
        {
            var voucher = new Voucher();
            decimal vDiscount = voucher.calculateDiscount(voucherCode, Subtotal);
            if (vDiscount > 0)
            {
                AppliedVoucherCode = voucherCode;
                VoucherDiscountAmount = vDiscount;
            }
            DiscountAmount = QuietDiscountAmount + VoucherDiscountAmount;
            FinalTotal = Math.Max(0m, Subtotal + DeliveryFee - DiscountAmount);
            return FinalTotal;
        }

        // UC3 (524H0031): Request online payment authorization
        public string authorizePayment(string paymentDetails)
        {
            OrderPayment ??= new Payment();
            AuthorizationCode = OrderPayment.authorizeOnlinePayment(paymentDetails, FinalTotal);
            return AuthorizationCode;
        }

        // UC3 (524H0031): Finalize order in state Placed, record payment, redeem voucher, queue station tickets
        public string completeOrder(string paymentMethod)
        {
            PaymentMethod = paymentMethod;
            OrderStatus = "Placed";
            OrderDateTime = DateTime.UtcNow;

            OrderPayment ??= new Payment();
            OrderPayment.OrderId = string.IsNullOrWhiteSpace(OrderId) ? "ORD-NEW" : OrderId;
            OrderPayment.recordPayment(paymentMethod, FinalTotal);

            if (!string.IsNullOrWhiteSpace(AppliedVoucherCode) && VoucherDiscountAmount > 0)
            {
                var voucher = VoucherDA.Instance.readVoucher(AppliedVoucherCode);
                voucher?.redeemVoucher();
            }

            Tickets.Clear();
            foreach (var stationType in Lines.Select(l => l.StationType).Distinct(StringComparer.OrdinalIgnoreCase))
            {
                var ticket = new KitchenTicket().createStationTicket(stationType);
                Tickets.Add(ticket);
            }

            OrderId = OrderDA.Instance.createOrder(this);
            OrderPayment.OrderId = OrderId;
            return OrderId;
        }

        public void UpdateStatus(string newStatus, string? reason = null)
        {
            OrderStatus = newStatus;
            if (newStatus == "Confirmed") IsLocked = true;
            if (newStatus == "Delivered") DeliveredAt = DateTime.UtcNow;
            if (newStatus == "Delivery_Failed" || newStatus == "Cancelled" || newStatus == "Rejected") CancellationReason = reason;
        }
    }
}
