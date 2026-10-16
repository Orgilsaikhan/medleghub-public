/**
 * Flowgorithm даалгаврын тест: схемийг тестийн оролтоор ажиллуулна.
 *
 * Оролтын мөр бүр нэг Input-д дарааллаараа очно — C/Python-ы stdin-тэй адил.
 * Харьцуулах гаралт нь `FlowRuntime.answer()`: сүүлчийн Input-ээс хойшх хэсэг,
 * тиймээс сурагч асуултаа хүссэнээрээ бичнэ.
 *
 * Энэ файл зөвхөн харьцангуй импорттой: `tests/flowgorithm.test.mjs` нь жишиг
 * шийдлүүдийг `tsc`-ээр хөрвүүлсэн ЯГ ЭНЭ кодоор шалгадаг.
 */

import type { FlowProgram } from "./model";
import { FlowRuntime, type RuntimeEvent } from "./runtime";

export interface FlowExecution {
  /** Сүүлчийн Input-ээс хойшх гаралт — харьцуулахаас өмнө хэвийн болгоно. */
  answer: string;
  /** Схем алдаагаар зогссон бол сурагчид харуулах тайлбар. */
  error?: string;
}

function reason(cause: unknown): string {
  return cause instanceof Error ? cause.message : "Схемийг ажиллуулж чадсангүй.";
}

export function executeFlow(program: FlowProgram, stdin: string): FlowExecution {
  const lines = stdin.replace(/\r\n?/g, "\n").split("\n");
  if (lines.at(-1) === "") lines.pop();

  let runtime: FlowRuntime;
  try {
    runtime = new FlowRuntime(program);
  } catch (cause) {
    return { answer: "", error: reason(cause) };
  }

  let used = 0;
  try {
    let result = runtime.iterator.next();
    while (!result.done) {
      // Unit тест `strict`-гүй tsc-ээр хөрвүүлдэг — `done`-оор нарийсгахгүй.
      const event = result.value as RuntimeEvent;
      if (event.kind !== "input") {
        result = runtime.iterator.next();
        continue;
      }
      const variable = event.variable!;
      if (used >= lines.length)
        throw new Error(
          `Тестийн оролт дууссан ч схем ${variable.name}-д дахин Input хүлээж байна. ` +
            "Даалгаварт хэдэн утга оруулахыг шалгана уу.",
        );
      const line = lines[used++];
      try {
        runtime.validateInput(variable.name, line);
      } catch (cause) {
        throw new Error(
          `«${line}» гэсэн тестийн оролтыг ${variable.name} (${variable.type}) хувьсагчид ` +
            `хадгалж чадсангүй: ${reason(cause)} Хувьсагчийн төрлөө шалгана уу.`,
        );
      }
      result = runtime.iterator.next(line);
    }
    return { answer: runtime.answer() };
  } catch (cause) {
    return { answer: runtime.answer(), error: reason(cause) };
  }
}
