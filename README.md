# Bitcoin Risk Metrics Dashboard

A real-time Bitcoin risk assessment dashboard built with Streamlit that provides key metrics to help evaluate Bitcoin's investment risk and market conditions.

## 🚀 Live Demo

View the live dashboard: [https://sheltered-springs-88934-ff25ba4be6be.herokuapp.com/]

## 📊 Features

### Risk Metrics
- **Price Index** - Power Law Bitcoin price percentile (0-100%)
- **Return Index** - Power Law Return Rate indicator (-3.1 to 3.1)
- **Volatility** - Current volatility percentage based on GARCH model (0-100%)

### Interactive Elements
- **Range Visualizations** - Color-coded horizontal bars showing 1-year ranges
- **30-Day Comparison** - Shows change from 30 days prior with trend indicators
- **Contextual Tooltips** - Hover (desktop) or tap (mobile) for detailed explanations

### Visual Indicators
- **Current Value** - Large circular markers showing present state
- **30d Prior Value** - Diamond markers indicating previous position
- **Color Coding** - Green to yellow to red gradient indicating risk levels
- **Trend Arrows** - Up/down arrows with color coding for 30-day changes

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **API Integration**: Requests
- **Styling**: Custom CSS with responsive design
- **Deployment**: Heroku (via Procfile)

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bitcoin-risk-dashboard.git
   cd bitcoin-risk-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Local URL: `http://localhost:8501`

## 🔧 Configuration

### API Endpoints
The dashboard fetches data from these endpoints:
- Bitcoin Price Data: `https://python-server-e4a8c032b69c.herokuapp.com/bitcoin-data`
- Volatility Data: `https://python-server-e4a8c032b69c.herokuapp.com/volatility`

### Customization
- **Metrics**: Modify the `get_data()` function to add/remove metrics
- **Colors**: Update the color scale in `get_color_from_scale()` function
- **Styling**: Adjust CSS in the Streamlit markdown sections
- **Ranges**: Configure min/max values for each metric in the data output

## 📁 File Structure

```
bitcoin-risk-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment configuration
├── README.md          # Project documentation
└── venv/             # Virtual environment (local)
```

## 🚀 Deployment

### Heroku Deployment
This app is configured for Heroku deployment with the included `Procfile`.

1. **Install Heroku CLI**
2. **Login to Heroku**
   ```bash
   heroku login
   ```
3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```
4. **Deploy**
   ```bash
   git push heroku main
   ```

### Alternative Deployment Options
- **Streamlit Cloud**: Connect your GitHub repository
- **Railway**: Deploy with automatic builds
- **Render**: Static site deployment

## 📊 Data Sources

The dashboard processes:
- **Historical Bitcoin prices** with quantile analysis
- **Volatility calculations** using GARCH modeling
- **Power Law Return Rate** for momentum assessment
- **30-day and 1-year comparative analysis**

## 🎨 UI/UX Features

- **Clean Interface**: Minimalist design focused on data clarity
- **Responsive Layout**: Adapts to different screen sizes
- **Interactive Tooltips**: Context-sensitive help system
- **Color-coded Indicators**: Intuitive risk level visualization
- **Hidden Streamlit Branding**: Clean, professional appearance

## 📱 Mobile Support

- Touch-friendly tooltip activation
- Responsive typography and spacing
- Optimized chart rendering for mobile screens
- Fast loading with efficient data processing

## 🔍 Metrics Explanation

### Price Index (0-100%)
Current Bitcoin price position relative to historical percentiles. Higher values indicate Bitcoin is expensive relative to its history.

### Return Index (-3.1 to 3.1)
Power Law Return Rate indicating momentum. Positive values suggest upward momentum, negative values indicate downward trends.

### Volatility (0-100%)
Current market volatility percentage. Higher values indicate more price uncertainty and risk.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bitcoin data provided by Yahoo Finance API.
- Built with Streamlit framework
- Visualization powered by Plotly.
- Based on my own research ([metashwin.com](https://metashwin.com))

## 📞 Support

For questions or issues:
- Open an issue in this repository
- Contact: [metashwin@proton.me]

---

**Disclaimer**: This dashboard is for educational and informational purposes only. It should not be considered financial advice. Always do your own research before making investment decisions. 