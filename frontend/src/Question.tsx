import { FC, use } from "react"

export type Question = { question: string; answers: string[] }
type Props = { questionsPromise: Promise<{ questions: Question[] }> }

export const QuestionCard: FC<Props> = ({ questionsPromise }) => {
    const { questions } = use(questionsPromise)
    const postAnswer = async (question: string, answer: string) =>{
        await fetch("http://localhost:5000/answer", {
            method: 'POST',
            body: JSON.stringify({
            question,
            answer
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    }
    return (
        <>
            {questions.map((e) => {
                return (
                    <div className="card">
                    <h2>{e.question}</h2>
                    <ul>
                        {e.answers.map((a) => {
                            return <Choice question={e.question} choice={a} onClick={postAnswer} />
                        })}
                    </ul>
                </div>
                )
            })}
        </>
    )
}

const Choice: FC<{ question: string, choice: string, onClick: (question: string, answer:string) => Promise<void> }> = ({ question, onClick, choice }) => {
    return (
        <li key={choice}>
            <button onClick={async () => await onClick(question, choice)}>{choice}</button>
        </li>
    )
}