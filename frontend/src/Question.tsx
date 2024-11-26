import { FC } from "react"

export type Question = { question: string; answers: string[] }
type Props = {
    questions: Question[];
    onAnswer: (question: string, answer: string) => void;
}

export const QuestionCard: FC<Props> = (props) => {

    return (
        <>
            {props.questions.map((e, i) => {
                return (
                    <div className="card" key={`${e.question}-${i}`}>
                        <h2>{e.question}</h2>
                        <ul>
                            {e.answers.map((a, j) => {
                                return (
                                    <li key={`${e.question}-choice-${j}`}>
                                        <button onClick={() => props.onAnswer(e.question, a)}>
                                            {a}
                                        </button>
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