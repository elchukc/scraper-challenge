import { FC, use } from "react"

export type Question = { question: string; answers: string[] }
type Props = { questionPromise: Promise<Question> }

export const QuestionCard: FC<Props> = ({ questionPromise }) => {
    const { question, answers } = use(questionPromise)
    return (
        <div className="card">
            <h2>{question}</h2>
            <ul>
                {answers.map((e) => {
                    return <Choice choice={e} />
                })}
            </ul>
        </div>
    )
}

const Choice: FC<{ choice: string }> = ({ choice }) => {
    return (
        <li>
            <button>{choice}</button>
        </li>
    )
}