import { useCallback, useEffect, useState } from 'react'
import { BsEyeglasses } from "react-icons/bs";
import './App.css'
import { Question, QuestionCard } from './Question';

function App() {
  const [aiQuestions, setAiQuestions] = useState<Question[]>([])
  const [survey, setSurvey] = useState<{question: string; answer: string}[]>([])
  const addQuestion = (question: string, answer: string) => {
    setSurvey((e) => [...e, {question, answer}])
  }

  const [category, setCategory] = useState<null|string>(null)
  const postCategorize = useCallback(async () => {
    const verdict = await fetch("http://localhost:5000/categorize", {
      method: 'POST',
      body: JSON.stringify(survey),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    setCategory(await verdict.json())
  }, [survey])

  const getAiQuestions = useCallback(async () => {
    const response = await fetch("http://localhost:5000/url")
    if (!response.ok) {
      throw new Error("Failed to fetch chatbot messages")
    }
    const res: { questions: Question[] } = await response.json()
    setAiQuestions(res.questions)
  }, [])

  useEffect(() => {
    getAiQuestions()
  }, [getAiQuestions])

  return (
    <>
      <div>
        <a href="https://bravecareer.notion.site/Mini-Challenge-Web-Scraper-for-Visitor-Classification-12966e26414d8047a44dc41fb4ad66d2" target="_blank">
          <BsEyeglasses className="logo" size={90} />
        </a>
        <h1>Paste a website url to see what our AI would ask</h1>
        <input name='scrape-url' placeholder='paste url here' autoFocus />
      </div>
      <br />
      <div className='board'>
        <QuestionCard questions={aiQuestions} onAnswer={addQuestion} />
      </div>
      {category
        ? <div className="read-the-docs">Your final stereotype: {category}</div>
        : <button onClick={async () => await postCategorize()}>Categorize me!</button>
      }
    </>
  )
}

export default App
