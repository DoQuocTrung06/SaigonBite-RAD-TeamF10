using SaigonBite.Controllers;

namespace SaigonBite.Views
{
    public class ReportConsoleUI
    {
        private readonly ReportController _controller;

        public ReportConsoleUI(ReportController controller)
        {
            _controller = controller;
        }

        public void RenderFilterForm(string hubs, string presets) => Console.WriteLine($"[UI] Filter Form: Hubs={hubs}, Presets={presets}");
        public void DisplayDashboard(string reportSummary) => Console.WriteLine($"[UI] Dashboard: {reportSummary}");
        public void OnGenerateReportClicked(string hubId, DateTime s, DateTime e) => _controller.GenerateReport(hubId, s, e);
        public string OnExportPDFClicked(string repId) => _controller.ExportToPDF(repId);
    }
}
