import { Suspense } from 'react'
import { BsEyeglasses } from "react-icons/bs";
import './App.css'
import { Question, QuestionCard } from './Question';

export const getAiQuestions: () => Promise<{ questions: Question[] }> = async () => {
  const response = await fetch("http://localhost:5000/url")
  if (!response.ok) {
    throw new Error("Failed to fetch chatbot messages")
  }
  return response.json()
}

function App() {

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
        <Suspense fallback={<div>Loading...</div>}>
          <QuestionCard questionsPromise={getAiQuestions()} />
        </Suspense>
      </div>
    </>
  )
}

export default App
