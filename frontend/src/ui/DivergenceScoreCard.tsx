

interface DivergenceScoreCardProps {
  score: number;
}

export function DivergenceScoreCard({ score }: DivergenceScoreCardProps) {
  const level = getLevel(score);
  const colors = getColors(level);

  return (
    <>
        {score < 0? "-" :
            <div
            className={`
                rounded-lg border p-2 text-center font-semibold text-xs min-w-[30px]
                ${colors.border} ${colors.bg} ${colors.text}
            `}
            >
            {level}
            </div>
        }
    </>
  );
}

function getLevel(score: number): "HIGH" | "MEDIUM" | "LOW" {
  if (score >= 0.60) return "HIGH";
  if (score >= 0.33) return "MEDIUM";
  return "LOW";
}

function getColors(level: "HIGH" | "MEDIUM" | "LOW") {
  switch (level) {
    case "HIGH":
      return {
        border: "border-red-700",
        bg: "bg-red-50",
        text: "text-red-500"
      };
    case "MEDIUM":
      return {
        border: "border-yellow-700",
        bg: "bg-yellow-50",
        text: "text-yellow-500"
      };
    case "LOW":
      return {
        border: "border-green-500",
        bg: "bg-green-50",
        text: "text-green-700"
      };
  }
}
