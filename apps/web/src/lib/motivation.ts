/**
 * Урам өгөх үгс.
 *
 * `MOTIVATIONS` — дасгалын тестэд 3 удаа дараалан унавал нэгийг нь санамсаргүй
 * харуулна (монгол, англиар). Хэрэглэгч «Тохиргоо»-ноос унтрааж болно.
 *
 * `PATH_QUOTES` — зөвхөн нууц `/footprints` хуудсанд. Хуудсыг нээх бүрд
 * нэгийг нь (өмнөхөөс өөрийг) харуулж, «Through Another's Path» тэмдэг олгоно.
 * Эх: `motivation.md`.
 */

export interface Motivation {
  /** Мөр бүр тусдаа — шилжүүлгийг хадгална. */
  mn: string[];
  en: string[];
}

/** Хэдэн удаа дараалан унасны дараа урам өгөх үг харуулах вэ. */
export const MOTIVATION_AFTER_FAILS = 3;

export const MOTIVATIONS: Motivation[] = [
  {
    en: [
      "You don't need to understand everything today.",
      "You just need to understand one thing more than yesterday.",
    ],
    mn: [
      "Өнөөдөр бүхнийг ойлгох албагүй.",
      "Өчигдрөөсөө ганцхан зүйлийг илүү ойлгоход л хангалттай.",
    ],
  },
  {
    en: ["Getting stuck isn't failing.", "Staying stuck because you stopped trying is."],
    mn: [
      "Гацах нь бүтэлгүйтэл биш.",
      "Харин оролдохоо болиод гацсан хэвээрээ үлдэх нь бүтэлгүйтэл.",
    ],
  },
  {
    en: ["Every error message is a clue.", "Read it. Think about it. Try again."],
    mn: ["Алдааны мессеж бүр нэг сэжүүр.", "Унш. Бод. Оролд."],
  },
  {
    en: [
      "Your code doesn't have to be perfect.",
      "It just has to be better than your last attempt.",
    ],
    mn: ["Код чинь төгс байх албагүй.", "Өмнөхөөсөө арай дээр байхад л болно."],
  },
  {
    en: ["The programmer you want to become", "is built by the bugs you refuse to give up on."],
    mn: ["Чиний болохыг хүсэж буй программист", "бууж өгөөгүй алдаа бүрээр чинь бүтдэг."],
  },
  {
    en: ["Don't think about the whole mountain.", "Just take the next step."],
    mn: ["Бүгдийг нэг дор бодох хэрэггүй.", "Дараагийн ганц алхмаа л хий."],
  },
  {
    en: ["If it's too much, make it smaller.", "One problem. One function. One line at a time."],
    mn: ["Хэтэрхий хүнд санагдвал жижиг болго.", "Нэг асуудал. Нэг функц. Нэг мөр."],
  },
  {
    en: ["It's okay to take a break.", "Rest is not quitting. Come back when you're ready."],
    mn: [
      "Түр завсарлаж бололгүй яах вэ?",
      "Амрах нь бууж өгч байгаа хэрэг биш. Бэлэн болсон үедээ буцаад ирэхэд болно.",
    ],
  },
  {
    en: ["Confused? Good.", "You're standing at the edge of something you haven't learned yet."],
    mn: [
      "Ойлгохгүй байна уу? Сайн байна.",
      "Чи хараахан сураагүй зүйлийнхээ өмнө зогсож байна л гэсэн үг.",
    ],
  },
  {
    en: ["You are not bad at coding. You're still learning."],
    mn: ["Чи код бичихдээ муу биш. Суралцаж байгаа төдий."],
  },
  {
    en: ["Slow progress is still progress."],
    mn: ["Удаан ахиц ч гэсэн ахиц шүү."],
  },
  {
    en: ["One more try."],
    mn: ["Дахиад нэг оролд."],
  },
  {
    en: ["Your future self will thank you for not quitting today."],
    mn: ["Өнөөдөр бууж өгөөгүйд чинь ирээдүйн чи баярлана."],
  },
  {
    en: ["You don't need motivation. Start small."],
    mn: ["Чамд заавал урам зориг хэрэггүй. Жижигхэн зүйлээс эхэл."],
  },
  {
    en: ["Debugging is just problem-solving with patience."],
    mn: ["Debug хийх гэдэг бол тэвчээртэйгээр асуудал шийдэхийг л хэлнэ."],
  },
  {
    en: ["Remember when this used to look impossible?", "Look how far you've already come."],
    mn: [
      "Өмнө нь энэ бүхэн боломжгүй мэт санагддаг байсныг сана.",
      "Аль хэдийн ямар хол явснаа хар даа.",
    ],
  },
  {
    en: ["You don't have to be the smartest person in the room.", "Be the one who keeps learning."],
    mn: [
      "Хүрээллийнхээ хамгийн ухаантай нь байх албагүй.",
      "Байнга үргэлжлүүлэн суралцдаг нь бай.",
    ],
  },
  {
    en: [
      "Nobody becomes a programmer by knowing everything.",
      "They become one by learning what they don't know.",
    ],
    mn: [
      "Бүхнийг мэддэг хүн программист болдоггүй.",
      "Мэдэхгүй бүхнээ сурсаар программист болдог.",
    ],
  },
  {
    en: ["Today's struggle can become tomorrow's", "“I finally get it.”"],
    mn: ["Өнөөдрийн зовлон чинь маргаашийн", "“Тийм байсан байна!” болж чадна."],
  },
  {
    en: ["Don't compare your chapter 2 to someone else's chapter 20."],
    mn: ["Өөрийнхөө 2-р бүлгийг бусдын 20-р бүлэгтэй бүү харьцуул."],
  },
];

/** Нууц хуудасны үгс — зөвхөн англиар. */
export const PATH_QUOTES: string[][] = [
  [
    "Nothing grows in comfort, we all grow in rain.",
    "If you want to get strong, you gotta endure all the pain.",
    "When things go wrong, you gotta keep your head straight.",
    "Make YOURSELF shine, don't wait for the light of day.",
  ],
  [
    "I know you don't want to study but,",
    "do you want the pain of discipline or the pain of regret?",
    "The pain of progress or the pain of regress?",
    "All along it's just you vs. yourself. Never forget that.",
  ],
  [
    "Do it anyway. Do it sad, do it mad, do it glad.",
    "Do it stressed, do it depressed, do it obsessed.",
  ],
  [
    "You might not have enough motivation today but,",
    "fall seven times, stand up eight my friend. Fight till success.",
  ],
  ["Smile at the pain, say you'll never break bro."],
  ["Rise and shine, live up to your name!"],
  [
    "You've spent enough time in your brain, same old thoughts, self refrain.",
    "Without action, it's all in vain. Now is the time to break the chain!",
    "One day or Day one.",
  ],
];

/** Үг бүрийн дараа налуу үсгээр. */
export const PATH_NOTE: string[] = [
  "Платформын энэ хэсгийг олсон таны сониуч занд талархъя.",
  "Таны урдах замаар би ч бас алхаж байсан. Энд байгаа урмын үгийг хайрлавал жаахан ч гэсэн ойлгохгүй, хэцүү байгаагаа мартаж дахин босож чадаасай гэж тавьсан юм. Жаахан хүнд ч гэсэн энэ замаар ганцаараа алхаагүй гэдгээ битгий мартаарай!",
];

export const PATH_BADGE_KEY = "through-anothers-path";

/** `0..length-1`-ээс санамсаргүй — `previous`-ээс өөр (давтагдахгүй). */
export function pickIndex(length: number, previous: number | null): number {
  if (length <= 1) return 0;
  const index = Math.floor(Math.random() * (length - (previous === null ? 0 : 1)));
  return previous !== null && index >= previous ? index + 1 : index;
}
