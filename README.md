# fuel-prices-agent
LangGraph AI Agent to answer the Gas Prices from Portugal Districts or Municipalities.
The agent uses the official API from the Portuguese Government to get the prices.
The default district and municipality is "Lisboa".
The default category of fuel is "Petrol".

## Available Tools/Features
- Search the web to get next week fuel prices changes
- Get fuel prices by brand, district and municipalities
- Get all portuguese districts
- Get all portuguese municipalities from a specific district
- Get all portuguese fuel brands
- Get all available currencies to convert prices
- Convert prices to a specific currency

## Example of Usage
```
Price of petrol in Lisbon?
```
```
Diesel price in Porto? Answer in a table format.
```
```
Gasoline price in Lagos for the brand Galp?
```
```
Prices of petrol in Lagos? please answer in bullets format, please include the current price and the next week expected price side by side
```
```
Prices of diesel in Faro? please answer in a table format including the price changes for next week.
```