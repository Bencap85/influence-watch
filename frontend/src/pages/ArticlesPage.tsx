import "../index.css";
import ArticleTable from "../components/ArticlesTable";


export default function ArticlesPage() {

  return (
    <div className="space-y-6">
      <ArticleTable articles={null} />
    </div>
  );
}
