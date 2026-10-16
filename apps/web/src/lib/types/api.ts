/**
 * Backend API-ийн response типүүд.
 *
 * Эдгээр нь `apps/api/app/schemas/`-тай тохирч байх ёстой. Backend schema
 * өөрчлөгдвөл энэ файлыг хамт шинэчилнэ.
 */

export type UserRole = "student" | "admin";

export type Difficulty = "beginner" | "intermediate" | "advanced";

export type Category =
  | "html_css"
  | "javascript"
  | "python"
  | "c"
  | "csharp"
  | "java"
  | "react"
  | "backend"
  | "database"
  | "git"
  | "flowgorithm";

// Monaco-ийн хэлний ID. Backend-ийн `LessonLanguage` enum-тай таарна.
export type LessonLanguage =
  | "javascript"
  | "jsx"
  | "html"
  | "css"
  | "python"
  | "c"
  | "cpp"
  | "shell"
  | "mysql"
  | "sql"
  | "plaintext";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  created_at: string;
  /** Standard багц хүчинтэй хугацаа. `null` бол хэзээ ч аваагүй. */
  plan_expires_at: string | null;
  /** Төлбөрт хичээлүүдийг үзэх эрхтэй эсэх (админ үргэлж `true`). */
  has_plan: boolean;
  /** Профайлын зургийн хувилбар. `null` бол зураггүй — `avatarUrl()`-ийг үз. */
  avatar_key: string | null;
  /** Бусад суралцагчийн жагсаалт, нийтийн профайлаас нуусан эсэх. */
  profile_hidden: boolean;
  /** Дасгалын тестэд 3 удаа дараалан унавал урам өгөх үг харуулах эсэх. */
  show_motivation: boolean;
  /** Бүртгэл бүрмөсөн устах мөч (хүсэлтээс 2 цагийн дараа). `null` бол хүсэлтгүй. */
  deletion_scheduled_at: string | null;
  /** Найзаа урих код — хэрэглэгчийн цэс, профайлд. */
  referral_code: string | null;
  /** Хичээлийн засварлагчийн байрлал («Тохиргоо»). */
  editor_layout: EditorLayout;
}

/** `new` — засварлагч зүүн, заавар баруун (React хичээлийнх шиг); `legacy` — заавар дээр. */
export type EditorLayout = "new" | "legacy";

export interface RegisterResult {
  /** `true` бол имэйл рүү код илгээсэн — баталгаажуулах хүртэл нэвтрээгүй. */
  verification_required: boolean;
  email: string;
  user: User | null;
}

export interface ChangeEmailResult {
  /** `true` бол шинэ хаяг руу код илгээсэн. */
  verification_required: boolean;
  user: User;
}

export interface CourseProgress {
  completed_lessons: number;
  total_lessons: number;
  percent: number;
}

export interface CourseSummary {
  id: string;
  title: string;
  slug: string;
  description: string;
  thumbnail_url: string | null;
  difficulty: Difficulty;
  category: Category;
  /** `true` бол бүх хичээл үнэгүй. */
  is_free: boolean;
  /** `is_free=false` үед эхний хэдэн хичээл үнэгүй вэ. */
  free_lessons: number;
  published: boolean;
  lesson_count: number;
  /** Секундээр. Хичээлүүдийн үргэлжлэх хугацааны нийлбэр. */
  duration: number;
  enrolled: boolean;
  progress: CourseProgress | null;
}

export interface LessonSummary {
  id: string;
  title: string;
  slug: string;
  duration: number;
  position: number;
  published: boolean;
  completed: boolean;
  /** Standard багц шаардлагатай. */
  locked: boolean;
}

export interface ModuleWithLessons {
  id: string;
  title: string;
  description: string;
  position: number;
  lessons: LessonSummary[];
}

export interface CourseDetail extends CourseSummary {
  created_at: string;
  updated_at: string;
  modules: ModuleWithLessons[];
}

export interface LessonTestCase {
  stdin: string;
  expected_output: string;
  /** Даалгаврын доор «Жишээ» болж харагдана. Бусад нь нууц. */
  sample: boolean;
  /**
   * React (`jsx`) хичээлийн DOM тест: нэр нь шаардлага болж харагдана,
   * `code` нь sandbox-ийн тест runtime дээр ажиллана. Бусад хэлд хоосон.
   */
  name?: string;
  code?: string;
}

/**
 * Дасгал. C/C++, Python — stdin/stdout-ийн HackerRank маягийн тест;
 * React — `name`/`code`-той DOM тест (react-tutorial.app маягаар).
 */
export interface LessonExercise {
  /** Markdown. */
  statement: string;
  tests: LessonTestCase[];
  /**
   * `answer` — SQL-ийн мөрдөгчийн хэрэг: тестгүй, сурагч олсон хариултаа
   * бичиж `POST /lessons/{id}/answer`-ээр шалгуулна. Хариулт хөтөчид ирдэггүй.
   */
  kind?: "tests" | "answer";
}

/** «Тусламж» — сурагч анхааруулгыг зөвшөөрсний дараа л авна. */
export interface LessonHelp {
  /** Markdown. */
  tips: string;
  solution: string;
}

export interface LessonDetail {
  id: string;
  module_id: string;
  title: string;
  slug: string;
  description: string;
  video_url: string | null;
  duration: number;
  /** Markdown. */
  content: string;
  initial_code: string;
  language: LessonLanguage;
  position: number;
  published: boolean;
  /** Бусдаасаа хэцүү хичээл — «Заавар» хэсэгт шар «Хэцүү» шошго. */
  challenging: boolean;
  exercise: LessonExercise | null;
  completed: boolean;
  /** Түгжигдсэн бол агуулга, код, дасгал, видео хоосон ирнэ. */
  locked: boolean;
}

export interface LessonLink {
  slug: string;
  title: string;
}

export interface LessonPlayer {
  course: { id: string; title: string; slug: string };
  lesson: LessonDetail;
  modules: ModuleWithLessons[];
  progress: CourseProgress;
  enrolled: boolean;
  previous_lesson: LessonLink | null;
  next_lesson: LessonLink | null;
}

export interface ContinueLink extends LessonLink {
  course_slug: string;
}

export interface MyCourse {
  course: CourseSummary;
  enrolled_at: string;
  progress: CourseProgress;
  continue_lesson: ContinueLink | null;
  last_completed_at: string | null;
}

export interface EnrollmentResult {
  course_id: string;
  enrolled_at: string;
  already_enrolled: boolean;
}

/** `completed` — ахиц хадгалагдсан (бүртгүүлсэн сурагч, зөв хариулт). */
export interface CaseAnswerResult {
  correct: boolean;
  completed: boolean;
  course_progress: CourseProgress | null;
  new_badges: BadgeUnlocked[];
}

export interface LessonCompleteResult {
  lesson_id: string;
  completed: boolean;
  completed_at: string | null;
  course_progress: CourseProgress;
  /** Энэ хичээлээр шинээр авсан тэмдгүүд. */
  new_badges: BadgeUnlocked[];
}

// --- Тэмдэг ба профайл ----------------------------------------------------------

export type BadgeShape = "circle" | "shield" | "hexagon";

export interface BadgeProgress {
  current: number;
  target: number;
}

export interface BadgeStatus {
  key: string;
  name: string;
  description: string;
  shape: BadgeShape;
  /** `false` — олгох өгөгдлийг одоогоор бүртгэдэггүй («Тун удахгүй»). */
  available: boolean;
  earned: boolean;
  /** Нууц амжилт — авах хүртэл `description` нь нөхцөлийг илчлэхгүй. */
  secret: boolean;
  /** Ховор амжилт — алтан гэрэлтэй харагдана. */
  rare: boolean;
  /** Алтан биш солонгон гэрэлтэй. */
  prismatic: boolean;
  awarded_at: string | null;
  progress: BadgeProgress | null;
  /** Нийт хэрэглэгчдийн хэдэн хувь нь авсан (0–100). Хэрэглэгч байхгүй бол `null`. */
  earned_percent: number | null;
  /** Нэрийн хажууд харуулах онцлох амжилтын байр (1–5). Сонгоогүй бол `null`. */
  showcase_position: number | null;
}

export interface BadgeUnlocked {
  key: string;
  name: string;
  description: string;
  shape: BadgeShape;
  secret: boolean;
  rare: boolean;
  /** Солонгон тэмдэг мэдэгдлийн оронд том цонхонд нээгдэнэ. */
  prismatic: boolean;
}

/** `new_badge` нь `null` бол аль хэдийн авсан. Бүтэн төлөв — том цонхонд харуулна. */
export interface BadgeClaimResult {
  new_badge: BadgeStatus | null;
}

export interface ProfileStats {
  completed_lessons: number;
  completed_exercises: number;
  completed_courses: number;
  enrolled_courses: number;
  earned_badges: number;
  total_badges: number;
}

export interface Profile {
  user: User;
  stats: ProfileStats;
  badges: BadgeStatus[];
}

// --- Бусад суралцагчид ----------------------------------------------------------

/** Бусдад харагдах хэрэглэгч — имэйл, эрх, багцын мэдээлэлгүй. */
export interface PublicUser {
  id: string;
  name: string;
  avatar_key: string | null;
  created_at: string;
}

export interface CourseStudent {
  id: string;
  name: string;
  avatar_key: string | null;
  /** Энэ сургалтын ахиц. */
  percent: number;
}

export interface CourseStudents {
  /** Бүх суралцагчийн тоо — `items` нь эхний хэсэг л байж болно. */
  total: number;
  items: CourseStudent[];
}

export interface ProfileCourse {
  slug: string;
  title: string;
  category: Category;
  progress: CourseProgress;
}

export interface PublicProfile {
  user: PublicUser;
  stats: ProfileStats;
  badges: BadgeStatus[];
  courses: ProfileCourse[];
}

// --- Санал хүсэлт ----------------------------------------------------------------

/** `report` — Community-ийн «Мэдэгдэх» товчоор л үүснэ, маягтаар илгээхгүй. */
export type FeedbackKind = "idea" | "bug" | "other" | "report";

export type FeedbackFormKind = Exclude<FeedbackKind, "report">;

export interface FeedbackInput {
  kind: FeedbackFormKind;
  message: string;
  /** Илгээх үеийн хуудасны зам (`/courses/python`). */
  page?: string | null;
}

export interface FeedbackItem {
  id: string;
  kind: FeedbackKind;
  message: string;
  page: string | null;
  resolved: boolean;
  created_at: string;
  user: Pick<User, "id" | "name" | "email">;
}

// --- Community -------------------------------------------------------------------

export type PostLanguage =
  | "python"
  | "c"
  | "cpp"
  | "javascript"
  | "html_css"
  | "sql"
  | "java"
  | "csharp"
  | "flowgorithm"
  | "general";

export type PostType = "discussion" | "help" | "fun_fact";

export interface PostAuthor {
  id: string;
  name: string;
  avatar_key: string | null;
  /** Нуусан бол профайл руу холбоос хийхгүй (403 буцаана). */
  profile_hidden: boolean;
}

interface PostBase {
  id: string;
  title: string;
  language: PostLanguage;
  type: PostType;
  pinned: boolean;
  /** `null` бол MedlegHub-ийн албан ёсны нийтлэл. */
  author: PostAuthor | null;
  created_at: string;
  like_count: number;
  comment_count: number;
  /** Одоогийн хэрэглэгч лайк дарсан эсэх. */
  liked: boolean;
}

export interface PostSummary extends PostBase {
  /** Markdown тэмдэгтгүй, нэг мөр богино хэсэг. */
  excerpt: string;
}

export interface CommentItem {
  id: string;
  body: string;
  created_at: string;
  author: PostAuthor;
}

export interface PostDetail extends PostBase {
  /** Markdown. */
  body: string;
  /** Хуучнаас нь шинэ рүү. */
  comments: CommentItem[];
}

export interface PostInput {
  title: string;
  body: string;
  language: PostLanguage;
  type: PostType;
}

export interface LikeResult {
  liked: boolean;
  like_count: number;
}

export type ReportReason = "spam" | "abuse" | "other";

/** Өөрт нь харагдах идэвхтэй түдгэлзүүлэлт. */
export interface SuspensionInfo {
  level: number;
  reason: string;
  created_at: string;
  /** `null` бол бүрмөсөн. */
  ends_at: string | null;
}

export interface CommunityStatus {
  guidelines_accepted: boolean;
  suspension: SuspensionInfo | null;
  /** Удаа тутмын түдгэлзүүлэх хоног; дууссаны дараагийн зөрчил бүрмөсөн. */
  suspension_days: number[];
}

export interface SuspensionItem {
  id: string;
  user: Pick<User, "id" | "name" | "email">;
  admin: Pick<User, "id" | "name"> | null;
  level: number;
  reason: string;
  created_at: string;
  ends_at: string | null;
  lifted_at: string | null;
  active: boolean;
}

export interface ReportInput {
  reason: ReportReason;
  details?: string | null;
}

// --- Standard багц --------------------------------------------------------

/** Нэг удаад авах хугацаа — 6 сар тутамд 1 сар үнэгүй (дүрмийг сервер тооцно). */
export interface PlanOption {
  months: number;
  free_months: number;
  /** Нийт дүн, бүхэл төгрөгөөр — үнэгүй сарыг тооцсон, хөнгөлөлтгүй. */
  price_mnt: number;
  /** Бодитоор төлөх дүн — хөнгөлөлт ба нэг удаагийн эрхийн үнэ байвал хасагдсан. */
  final_price_mnt: number;
  /** Үүний нэг удаагийн эрхийн үнээс хасагдах хэсэг (`PlanStatus.upgrade_credit`). */
  credit_mnt: number;
}

/**
 * Нэг удаагийн Live эрх авснаас хойш `live_pass_upgrade_days` хоногийн дотор
 * Standard/Premium авбал эрхийн үнэ хасагдана. `options`-ийн үнэд аль хэдийн орсон.
 */
export interface UpgradeCredit {
  amount_mnt: number;
  expires_at: string;
}

/** Checkout-д орох хөнгөлөлт. Нэг төлбөрт нэг л хөнгөлөлт. */
export interface PlanDiscount {
  /** `promo` — оруулсан промо код; `referral` — урилгын кодоор бүртгүүлсний хөнгөлөлт. */
  source: "promo" | "referral";
  percent_off: number;
  code: string | null;
}

export interface PlanStatus {
  has_plan: boolean;
  plan_expires_at: string | null;
  /** Сарын үнэ, бүхэл төгрөгөөр. */
  price_mnt: number;
  /** 1–12 сар, тус бүрийн нийт үнэ. */
  options: PlanOption[];
  /**
   * Промо код оруулаагүй бол дараагийн төлбөрт автоматаар орох урилгын хөнгөлөлт —
   * урилгын кодоор бүртгүүлсэн, хараахан ашиглаагүй хэрэглэгчид.
   */
  discount: PlanDiscount | null;
  /**
   * Premium = Standard + MedlegHub Live-ийн илүү AI. Live бүгдэд нээлттэй (эсвэл
   * админ) үед л зарна — `false` бол Premium-ийг харуулахгүй.
   */
  premium_available: boolean;
  premium_price_mnt: number;
  /** 1–12 сар; Premium зарагдахгүй бол хоосон. */
  premium_options: PlanOption[];
  has_premium: boolean;
  premium_expires_at: string | null;
  /** MedlegHub Live-ийн сарын материалын хязгаар (серверийн тохиргоо). */
  /** Premium нь Standard-аас Live-д хэд дахин их хэрэглээтэй. */
  premium_usage_multiplier: number;
  /**
   * Нэг удаагийн Live эрх — нэг материал. Premium шиг Live бүгдэд нээлттэй (эсвэл
   * админ) үед л зарна. Зочин ч үнийг харна; авахын тулд нэвтэрнэ.
   */
  live_pass_available: boolean;
  live_pass_price_mnt: number;
  /** Ашиглаагүй эрхтэй бол дахин авахгүй. */
  has_unused_live_pass: boolean;
  upgrade_credit: UpgradeCredit | null;
  /** Эрхийг материалд ашигласнаас хойш хэдэн хоног нээлттэй. */
  live_pass_access_days: number;
  /** Эрх авснаас хойш хэдэн хоногт багц авбал эрхийн үнэ хасагдах. */
  live_pass_upgrade_days: number;
}

/** `live_pass` — багц биш, нэг материалд зориулсан нэг удаагийн Live эрх. */
export type BillingPlan = "standard" | "premium" | "live_pass";

export type PromoKind = "percent" | "free_months";

/** Оруулсан промо код хүчинтэй — юу өгөх, хувийн код бол хөнгөлөлттэй үнэ. */
export interface PromoPreview {
  code: string;
  kind: PromoKind;
  percent_off: number | null;
  free_months: number | null;
  expires_at: string | null;
  /** Хувийн кодод 1–12 сарын хөнгөлөлттэй үнэ, үнэгүй сарын кодод хоосон. */
  options: PlanOption[];
  /** Мөн Premium-д (Premium зарагдаж байвал). */
  premium_options: PlanOption[];
}

export type PromoStatus = "active" | "disabled" | "expired" | "used_up";

/** Админд: нэг промо код, ашигласан тоотой. */
export interface PromoCodeItem {
  id: string;
  code: string;
  kind: PromoKind;
  percent_off: number | null;
  free_months: number | null;
  expires_at: string | null;
  max_uses: number | null;
  active: boolean;
  note: string | null;
  uses: number;
  status: PromoStatus;
  created_at: string;
  /** Үүсгэсэн админы нэр. Бүртгэл нь устсан бол `null`. */
  created_by: string | null;
}

export interface PromoCodeInput {
  /** Хоосон бол сервер санамсаргүй 8 тэмдэгт үүсгэнэ. */
  code: string | null;
  kind: PromoKind;
  percent_off: number | null;
  free_months: number | null;
  expires_at: string | null;
  max_uses: number | null;
  note: string | null;
}

/** Найзаа урих: өөрийн код ба олсон шагнал (зөвхөн нийт тоо). */
export interface ReferralSummary {
  code: string;
  /** Кодоор бүртгүүлсэн найзын нэг удаагийн хөнгөлөлт (хувь). */
  friend_percent_off: number;
  /** Урьсан найзуудаас `friends_per_reward` нь багц авах бүрд `reward_months` сар. */
  friends_per_reward: number;
  reward_months: number;
  /** Имэйлээ баталгаажуулсан найзын тоо. */
  friends: number;
  /** Дор хаяж нэг удаа төлсөн найзын тоо. */
  paying_friends: number;
  /** Дараагийн үнэгүй сар хүртэл дахиад хэдэн найз багц авах вэ. */
  friends_to_next_reward: number;
  months_earned: number;
}

/** Админд: Standard багцын одоогийн сарын үнэ ба түүнийг хэн, хэзээ тавьсан. */
export interface PlanPriceInfo {
  /** Сарын үнэ, бүхэл төгрөгөөр. */
  price_mnt: number;
  /** Админ хэзээ ч өөрчлөөгүй бол ашиглагдах үнэ (`PLAN_PRICE_MNT`). */
  default_price_mnt: number;
  /** Анхдагч үнэ хэрэглэгдэж байвал `null`. */
  changed_at: string | null;
  changed_by: string | null;
  premium_price_mnt: number;
  premium_default_price_mnt: number;
  premium_changed_at: string | null;
  premium_changed_by: string | null;
  /** Нэг удаагийн Live эрхийн үнэ (сарынх биш). */
  live_pass_price_mnt: number;
  live_pass_default_price_mnt: number;
  live_pass_changed_at: string | null;
  live_pass_changed_by: string | null;
}

/** Админд: багцыг гараар өөрчилсөн нэг удаа. `months` > 0 бол нэмсэн, < 0 бол хассан. */
export interface PlanAdjustment {
  id: string;
  months: number;
  expires_before: string | null;
  expires_after: string;
  note: string | null;
  /** Өөрчилсөн админ. Бүртгэл нь устсан бол `null`. */
  admin_name: string | null;
  created_at: string;
}

/** Админд: хэрэглэгчийн багц ба гараар хийсэн сүүлийн өөрчлөлтүүд (шинэ нь эхэндээ). */
export interface AdminUserPlan {
  user_id: string;
  name: string;
  email: string;
  has_plan: boolean;
  plan_expires_at: string | null;
  adjustments: PlanAdjustment[];
}

export interface CheckoutSession {
  payment_id: string;
  /** `pay.wire.mn` дээрх төлбөрийн хуудас. */
  checkout_url: string;
}

export type PaymentState = "pending" | "succeeded" | "canceled" | "failed";

/** Амжилттай төлбөр эсвэл үнэгүй сарын промо кодын баримт — `/billing/success`. */
export interface PaymentReceipt {
  /** `payment` — Wire-ээр төлсөн; `promo` — үнэгүй сарын промо код (0₮). */
  kind: "payment" | "promo";
  plan: BillingPlan;
  /** Нэг удаагийн эрхэд 0. */
  months: number;
  free_months: number;
  /** Хөнгөлөлтийн өмнөх дүн = `amount_mnt` + `discount_mnt` + `credit_mnt`. */
  list_price_mnt: number;
  discount_percent: number;
  discount_mnt: number;
  /** Нэг удаагийн эрхийн үнээс хасагдсан дүн. */
  credit_mnt: number;
  discount_source: "promo" | "referral" | null;
  promo_code: string | null;
  /** Бодитоор төлсөн дүн. */
  amount_mnt: number;
  currency: string;
  /** Wire-ийн гүйлгээний дугаар (`pi_…`). */
  reference: string | null;
  created_at: string;
  paid_at: string | null;
}

export interface PaymentStatus {
  id: string;
  status: PaymentState;
  plan: PlanStatus;
  /** Зөвхөн `succeeded` үед. */
  receipt: PaymentReceipt | null;
}

/** Үнэгүй сарын кодыг идэвхжүүлсний дараах багц ба баримтын id. */
export interface PromoRedeemResult extends PlanStatus {
  redemption_id: string;
}

/** Үнэгүй сарын промо кодын баримт. */
export interface RedemptionReceipt {
  id: string;
  plan: PlanStatus;
  receipt: PaymentReceipt;
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface MessageResult {
  message: string;
}

// --- Admin payloads -------------------------------------------------------

export interface CourseInput {
  title: string;
  slug: string;
  description?: string;
  thumbnail_url?: string | null;
  difficulty?: Difficulty;
  category?: Category;
  is_free?: boolean;
  free_lessons?: number;
  published?: boolean;
}

export interface ModuleInput {
  title: string;
  description?: string;
  position?: number;
}

export interface LessonInput {
  title: string;
  slug: string;
  description?: string;
  video_url?: string | null;
  duration?: number;
  content?: string;
  initial_code?: string;
  language?: LessonLanguage;
  position?: number;
  published?: boolean;
}

export type AnnouncementKind = "update" | "feature";
/** `everyone` — нэвтрээгүй зочин ч; `free` — багцгүй; `standard` — багцтай хэрэглэгч. */
export type AnnouncementAudience = "everyone" | "signed_in" | "free" | "standard";

/** Хэрэглэгчид гарах зарлалын цонх. */
export interface Announcement {
  id: string;
  kind: AnnouncementKind;
  title: string;
  /** Markdown — HTML, зураггүй. */
  body: string;
  /** Товч — хоёулаа эсвэл аль нь ч биш. Холбоос нь `/…` эсвэл `https://…`. */
  cta_label: string | null;
  cta_url: string | null;
}

export type AnnouncementStatus = "draft" | "scheduled" | "live" | "ended";

/** Админд: зарлалын бүх тохиргоо ба төлөв. */
export interface AnnouncementItem extends Announcement {
  audience: AnnouncementAudience;
  starts_at: string | null;
  ends_at: string | null;
  active: boolean;
  status: AnnouncementStatus;
  created_at: string;
  updated_at: string;
  /** Бичсэн админы нэр. Бүртгэл нь устсан бол `null`. */
  created_by: string | null;
}

export type AnnouncementInput = Omit<
  AnnouncementItem,
  "id" | "status" | "created_at" | "updated_at" | "created_by"
>;
