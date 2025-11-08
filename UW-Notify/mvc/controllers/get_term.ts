import { cancelAllScheduledNotificationsAsync } from "expo-notifications";

export function get_term() {
  const date = new Date()

  let year = date.getFullYear();
  const month = date.getMonth(); // 0 = Jan, 11 = Dec
  console.log(`${year} ${month}`)
  let termDigit: 1 | 5 | 9;
  if (6 <= month && month <= 9) termDigit = 9;           // Sep–Dec: Fall
  else if (2 <= month && month <= 5) termDigit = 5;      // May–Aug: Spring
  else termDigit = 1;                      // Jan–Apr: Winter

  if (month >= 10) {
    year += 1
  }

  return (year - 1900) * 10 + termDigit;
}

export function term_to_str(term: number) {
  const season = term%10;
  const year = (term-season)/10+1900

  let season_str = ""
  if (season === 1) {
    season_str = "Winter"
  }
  else if (season === 5){ 
    season_str = "Spring"
  }
  else {
    season_str = "Fall"
  }

  const term_str = `${season_str} ${year}`

  return term_str
}