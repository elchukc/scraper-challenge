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
            {questions.map((e, i) => {
                return (
                    <div className="card" key={`${e.question}-${i}`}>
                        <h2>{e.question}</h2>
                        <ul>
                            {e.answers.map((a, j) => {
                                return (
                                    <li key={`${e.question}-choice-${j}`}>
                                        <button onClick={async () => {
                                            await postAnswer(e.question, a)
                                        }}>{a}</button>
                                    </li>
                                )
                            })}
                        </ul>
                    </div>
                )
            })}
        </>
    )
}