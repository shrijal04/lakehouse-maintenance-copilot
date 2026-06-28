import RecommendationCard from "./RecommendationCard";

interface Recommendation {
  id: number;
  title: string;
  description: string;
  priority: string;
}

interface Props {
  recommendations: Recommendation[];
}

export default function Recommendations({
  recommendations,
}: Props) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        AI Recommendations
      </h2>

      <div className="space-y-4">
        {recommendations.map((item) => (
          <RecommendationCard
            key={item.id}
            title={item.title}
            description={item.description}
            priority={item.priority}
          />
        ))}
      </div>
    </div>
  );
}