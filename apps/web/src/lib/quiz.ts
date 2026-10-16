/**
 * Хичээлийн доторх «Шалгах асуулт» — Markdown-д ```quiz блокоор бичнэ:
 *
 *     ```quiz
 *     Дараах кодын дараа `count` хэд болох вэ?
 *     - [ ] 2
 *     - [x] 1
 *     > Хоёр дуудалт хоёулаа ижил `count` (0)-оос тооцно.
 *     ```
 *
 * `- [x]` нь зөв хариулт. Хэд хэдэн `[x]` байвал олон сонголттой. `>`-оор
 * эхэлсэн мөрүүд тайлбар — зөв хариулсны дараа харагдана.
 */

export interface QuizOption {
  text: string;
  correct: boolean;
}

export interface Quiz {
  question: string;
  options: QuizOption[];
  explanation: string;
}

const OPTION = /^\s*[-*] \[( |x|X)\] (.*)$/;

export function parseQuiz(source: string): Quiz | null {
  const question: string[] = [];
  const options: QuizOption[] = [];
  const explanation: string[] = [];

  for (const line of source.replace(/\r\n?/g, "\n").split("\n")) {
    const option = OPTION.exec(line);
    if (option) {
      options.push({ text: option[2].trim(), correct: option[1].toLowerCase() === "x" });
    } else if (line.startsWith(">")) {
      explanation.push(line.replace(/^>\s?/, ""));
    } else if (options.length === 0) {
      question.push(line);
    }
  }

  const text = question.join("\n").trim();
  if (!text || options.length < 2 || !options.some((option) => option.correct)) return null;
  return { question: text, options, explanation: explanation.join("\n").trim() };
}
