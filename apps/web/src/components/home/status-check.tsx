"use client"

import { useState } from "react"
import { FileSearch } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function StatusCheck() {
  const [applicationNumber, setApplicationNumber] = useState("")

  return (
    <Card className="h-full">
      <CardContent className="flex h-full flex-col gap-4">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <FileSearch className="size-5" />
        </div>
        <div>
          <h3 className="text-lg font-semibold">Track application</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Enter the application number to check its current status.
          </p>
        </div>
        <div className="mt-auto flex min-w-0 gap-2">
          <Input
            placeholder="Application number"
            aria-label="Application number"
            className="h-9 min-w-0 flex-1 text-sm"
            value={applicationNumber}
            onChange={(e) => setApplicationNumber(e.target.value)}
          />
          <Button size="sm" variant="outline" className="h-9">
            Check status
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
