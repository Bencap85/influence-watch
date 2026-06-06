import type { CountryCode } from '../constants/countryCode';
import { countryCodeToFlagCode } from '../constants/countryCodeToFlag';

interface CountryListProps {
    countries: string[]
}

export default function CountryList({ countries }: CountryListProps) {
  return (
    <div className="flex flex-wrap gap-4 justify-end">
      {countries.map(code => (
        <div key={code} className="flex items-center gap-1.5">
          <span className={`fi fi-${countryCodeToFlagCode[code as CountryCode]?.toLowerCase()}`} />
          <span className="">{code}</span>
        </div>
      ))}
    </div>
  );
}
