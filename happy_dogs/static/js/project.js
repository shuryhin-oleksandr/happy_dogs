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
      <div className="form-row mb-4">
        <div className="col-auto">
          <label className="sr-only" htmlFor="inlineFormInput">Name</label>
          <div className="input-group mb-2">
            <div className="input-group-prepend">
              <div className="input-group-text">Start date</div>
            </div>
            <input type="text" className="form-control" value={boardingStartDate}
                   onChange={(e) => setBoardingStartDate(e.target.value)}/>
          </div>
        </div>
        <div className="col-auto">
          <label className="sr-only" htmlFor="inlineFormInputGroup">Username</label>
          <div className="input-group mb-2">
            <div className="input-group-prepend">
              <div className="input-group-text">End date</div>
            </div>
            <input type="text" className="form-control" value={boardingEndDate}
                   onChange={(e) => setBoardingEndDate(e.target.value)}/>
          </div>
        </div>
      </div>
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
    return (
      <div>
        <h3>Boarding</h3>
        <div className="list-group">
          {boarding_records.map((boarding_record, index) => (
            <a href="#" className="list-group-item list-group-item-action py-1" key={index}
               onClick={(e) => setBoardingDayUrl(boarding_record.url)}>
              {boarding_record.date} - {boarding_record.dogs_count}
            </a>
          ))}
        </div>
      </div>
    )
  }
}

const BoardingDay = ({boardingDayUrl}) => {
  const [error, isLoaded, items] = useFetchAPI(boardingDayUrl)

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <div>
        <h3>Boarding visits</h3>
        <ul className="list-group">
          {items.map((item, index) => (
            <li className="list-group-item py-1" key={index}>
              {item.dog}: {item.start_date} - {item.end_date}
            </li>
          ))}
        </ul>
      </div>
    )
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
    <div className="container py-5">
      <BoardingFilterForm
        boardingStartDate={boardingStartDate}
        boardingEndDate={boardingEndDate}
        setBoardingStartDate={setBoardingStartDate}
        setBoardingEndDate={setBoardingEndDate}/>
      <div className="row">
        <div className="col-3">
          <Boarding
            setBoardingDayUrl={setBoardingDayUrl}
            boardingStartDate={boardingStartDate}
            boardingEndDate={boardingEndDate}/>
        </div>
        <div className="col-6">
          <BoardingDay boardingDayUrl={boardingDayUrl}/>
        </div>
      </div>
    </div>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>,
  document.getElementById('root')
);
