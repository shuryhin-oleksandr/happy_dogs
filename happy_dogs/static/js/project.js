const host = window.location.protocol + "//" + window.location.host;

const useFetchAPI = (url) => {
  const [error, setError] = React.useState(null);
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [items, setItems] = React.useState([]);

  console.log(url)

  React.useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [url])
  return [error, isLoaded, items];
}

const BoardingFilterForm = ({boardingStartDate, boardingEndDate, setBoardingStartDate, setBoardingEndDate}) => {
  return (
    <div>
      <p>
        <label htmlFor="id_start_date">Start date:</label>
        <input
          type="text"
          value={boardingStartDate}
          onChange={(e) => setBoardingStartDate(e.target.value)}
        />
      </p>
      <p>
        <label htmlFor="id_end_date">End date:</label>
        <input
          type="text"
          value={boardingEndDate}
          onChange={(e) => setBoardingEndDate(e.target.value)}
        />
      </p>
    </div>
  )
}

const Boarding = ({setBoardingDayUrl, boardingStartDate, boardingEndDate}) => {
  const [error, isLoaded, items] =
    useFetchAPI(`/dogs/boarding-api/?start_date=${boardingStartDate}&end_date=${boardingEndDate}`)

  let boarding_records = [...items];
  boarding_records.forEach((boarding_record) => {
    boarding_record.url = `${host}/dogs/boarding-api/${boarding_record.date.replaceAll('-', '/')}/`
  })

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (boarding_records.map((boarding_record, index) => (
      <div key={index} onClick={(e) => setBoardingDayUrl(boarding_record.url)}>
        {boarding_record.date} - {boarding_record.dogs_count}
      </div>
    )))
  }
}

const BoardingDay = ({boardingDayUrl}) => {
  const [error, isLoaded, items] = useFetchAPI(boardingDayUrl)

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (items.map((item, index) => (
      <div key={index}>
        {item.dog}: {item.start_date} - {item.end_date}
      </div>
    )))
  }
}

const App = () => {
  let date = new Date(), year = date.getFullYear(), month = date.getMonth();
  let firstMonthDay = new Date(year, month, 2);
  let lastMonthDay = new Date(year, month + 1, 1);
  let firstMonthDayStr = firstMonthDay.toISOString().split('T')[0]
  let lastMonthDayStr = lastMonthDay.toISOString().split('T')[0]

  const [boardingDayUrl, setBoardingDayUrl] = React.useState(
    `/dogs/boarding-api/${firstMonthDayStr.replaceAll('-', '/')}/`
  )
  const [boardingStartDate, setBoardingStartDate] = React.useState(firstMonthDayStr)
  const [boardingEndDate, setBoardingEndDate] = React.useState(lastMonthDayStr)

  return (
    <div>
      <BoardingFilterForm
        boardingStartDate={boardingStartDate}
        boardingEndDate={boardingEndDate}
        setBoardingStartDate={setBoardingStartDate}
        setBoardingEndDate={setBoardingEndDate}/>
      <Boarding
        setBoardingDayUrl={setBoardingDayUrl}
        boardingStartDate={boardingStartDate}
        boardingEndDate={boardingEndDate}/>
      <BoardingDay boardingDayUrl={boardingDayUrl}/>
    </div>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>,
  document.getElementById('root')
);
