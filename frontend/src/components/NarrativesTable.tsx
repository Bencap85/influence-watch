import { Table } from "../ui/Table";
import type { Narrative } from "../types/detection";
import { countryCodeToFlagCode } from "../constants/countryCodeToFlag";
import type { CountryCode } from "../constants/countryCode";

interface NarrativesTableProps {
  narratives: Narrative[] | undefined;
}

export default function NarrativesTable({ narratives }: NarrativesTableProps) {
  if (!narratives) return <div>Loading...</div>;

  return (
    <Table<Narrative>
      data={narratives}
      columns={[
        {
          key: "country_code",
          label: "Country",
          render: (n) => (
            <div className="flex items-center gap-2">
              <span
                className={`fi fi-${countryCodeToFlagCode[n.country_code]?.toLowerCase()}`}
              />
              <span className="text-stone-600">{n.country_code}</span>
            </div>
          )
        },
        {
          key: "keywords",
          label: "Keywords",
          render: (n) =>
            n.keywords.length > 0 ? n.keywords.join(", ") : "—"
        },
        {
          key: "divergence",
          label: "Divergence Score",
          render: (n) => {
            return (
              <>
                <span className="font-mono text-stone-600">
                  {n.divergence_from_world}
                </span>
              </>
              );
            // const divergence = n.divergence;
            // if (!divergence) return null;

            // const sorted = Object.entries(divergence)
            //   .sort(([, a], [, b]) => a - b);

            // const list = sorted.map(([key, value]) => `${key}: ${value}`);

            // if (list.length <= 1) return null;

            // const closest = {
            //   countryCode: list[1].split(": ")[0] as CountryCode,
            //   divergence: list[1].split(": ")[1]
            // }

            // const farthest = {
            //   countryCode: list[list.length - 1].split(": ")[0] as CountryCode,
            //   divergence: list[list.length - 1].split(": ")[1]
            // }

            // return (
            //   <div>
            //     <span className="font-mono text-stone-600">
            //       {"Closest: "}
            //     </span>
            //     <div className="inline-flex items-center gap-1">
            //       <span className={`fi fi-${countryCodeToFlagCode[closest.countryCode]?.toLowerCase()}`} />
            //       {closest.countryCode}
            //       <span className="font-mono text-green-600">({closest.divergence})</span>
            //      </div>
            //     <br />
            //     <span className="font-mono text-stone-600">
            //       {"Farthest: "}
            //     </span>
            //     <div className="inline-flex items-center gap-1">
            //       <span className={`fi fi-${countryCodeToFlagCode[farthest.countryCode]?.toLowerCase()}`} />
            //       {farthest.countryCode}
            //       <span className="font-mono text-red-600">({farthest.divergence})</span>
            //      </div>
            //   </div>)
          }
        }
      ]}
      rowKey={(n) => n.id}
    />
  );
}
