import React, { type ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import { Citation } from "../ui/Citation";
import type { SourceItem } from "../types/source/sourceItem";

export function BriefRenderer({ briefResponse }) {

  const {brief, sources} = briefResponse;

  return (
    <ReactMarkdown
      components={{
        p: ({ children }) => <p>{processChildren(children, sources)}</p>,
        span: ({ children }) => <span>{processChildren(children, sources)}</span>,
        li: ({ children }) => <li>{processChildren(children, sources)}</li>,
        strong: ({ children }) => <strong>{processChildren(children, sources)}</strong>,
        em: ({ children }) => <em>{processChildren(children, sources)}</em>,
        h1: ({ children }) => <h1>{processChildren(children, sources)}</h1>,
        h2: ({ children }) => <h2>{processChildren(children, sources)}</h2>,
        h3: ({ children }) => <h3 className="font-semibold">{processChildren(children, sources)}</h3>,
      }}
    >
      {brief}
    </ReactMarkdown>
  );
}

function processChildren(children: ReactNode, sources: Record<string, SourceItem>): ReactNode {
  if (typeof children === "string") {
    return splitAndReplaceCitations(children, sources);
  }

  if (Array.isArray(children)) {
    return children.map((child, i) => (
      <React.Fragment key={i}>{processChildren(child, sources)}</React.Fragment>
    ));
  }

  if (React.isValidElement(children)) {
    return React.cloneElement(children, {
      ...children.props,
      children: processChildren(children.props.children, sources),
    });
  }

  return children;
}

function splitAndReplaceCitations(text: string, sources: Record<string, SourceItem>) {
  const parts = text.split(/(\[\d+\])/g);

  return parts.map((part, i) => {
    const match = part.match(/^\[(\d+)\]$/);
    if (match) {
      const id = match[1];
      const source = sources[id];
      if (!source) return part;
      return <Citation key={i} id={id} source={source} />;
    }
    return <React.Fragment key={i}>{part}</React.Fragment>;
  });
}

