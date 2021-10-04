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

const Boarding = ({setBoardingDayUrl}) => {
  const [error, isLoaded, items] = useFetchAPI('/dogs/boarding-api/')

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
  const [boardingDayUrl, setBoardingDayUrl] = React.useState('/dogs/boarding-api/2021/10/5/')
  return (
    <div>
      <Boarding setBoardingDayUrl={setBoardingDayUrl}/>
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
