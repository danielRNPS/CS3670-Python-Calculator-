"use client"

import { useState, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Delete, Divide, X, Minus, Plus, Equal, Percent } from "lucide-react"

export function Calculator() {
  const [display, setDisplay] = useState("0")
  const [expression, setExpression] = useState("")
  const [hasResult, setHasResult] = useState(false)

  const handleNumber = useCallback((num: string) => {
    if (hasResult) {
      setDisplay(num)
      setExpression("")
      setHasResult(false)
    } else if (display === "0" && num !== ".") {
      setDisplay(num)
    } else if (num === "." && display.includes(".")) {
      return
    } else {
      setDisplay(display + num)
    }
  }, [display, hasResult])

  const handleOperator = useCallback((op: string) => {
    setExpression(display + " " + op)
    setDisplay("0")
    setHasResult(false)
  }, [display])

  const handleEquals = useCallback(() => {
    if (!expression) return
    
    const fullExpression = expression + " " + display
    try {
      // Replace display operators with JS operators
      const evalExpression = fullExpression
        .replace(/×/g, "*")
        .replace(/÷/g, "/")
        .replace(/%/g, "/100")
      
      // Use Function constructor for safer evaluation
      const result = new Function(`return ${evalExpression}`)()
      
      // Format the result
      const formattedResult = Number.isInteger(result) 
        ? result.toString() 
        : parseFloat(result.toFixed(10)).toString()
      
      setDisplay(formattedResult)
      setExpression(fullExpression + " =")
      setHasResult(true)
    } catch {
      setDisplay("Error")
      setExpression("")
      setHasResult(true)
    }
  }, [display, expression])

  const handleClear = useCallback(() => {
    setDisplay("0")
    setExpression("")
    setHasResult(false)
  }, [])

  const handleDelete = useCallback(() => {
    if (hasResult) {
      handleClear()
    } else if (display.length > 1) {
      setDisplay(display.slice(0, -1))
    } else {
      setDisplay("0")
    }
  }, [display, hasResult, handleClear])

  const handlePercent = useCallback(() => {
    const value = parseFloat(display) / 100
    setDisplay(value.toString())
  }, [display])

  const handleNegate = useCallback(() => {
    if (display !== "0") {
      setDisplay(display.startsWith("-") ? display.slice(1) : "-" + display)
    }
  }, [display])

  const buttons = [
    { label: "AC", action: handleClear, variant: "secondary" as const },
    { label: "±", action: handleNegate, variant: "secondary" as const },
    { label: <Percent className="size-5" />, action: handlePercent, variant: "secondary" as const },
    { label: <Divide className="size-5" />, action: () => handleOperator("÷"), variant: "accent" as const },
    { label: "7", action: () => handleNumber("7"), variant: "default" as const },
    { label: "8", action: () => handleNumber("8"), variant: "default" as const },
    { label: "9", action: () => handleNumber("9"), variant: "default" as const },
    { label: <X className="size-5" />, action: () => handleOperator("×"), variant: "accent" as const },
    { label: "4", action: () => handleNumber("4"), variant: "default" as const },
    { label: "5", action: () => handleNumber("5"), variant: "default" as const },
    { label: "6", action: () => handleNumber("6"), variant: "default" as const },
    { label: <Minus className="size-5" />, action: () => handleOperator("-"), variant: "accent" as const },
    { label: "1", action: () => handleNumber("1"), variant: "default" as const },
    { label: "2", action: () => handleNumber("2"), variant: "default" as const },
    { label: "3", action: () => handleNumber("3"), variant: "default" as const },
    { label: <Plus className="size-5" />, action: () => handleOperator("+"), variant: "accent" as const },
    { label: "0", action: () => handleNumber("0"), variant: "default" as const, span: true },
    { label: ".", action: () => handleNumber("."), variant: "default" as const },
    { label: <Equal className="size-5" />, action: handleEquals, variant: "primary" as const },
  ]

  return (
    <div className="w-full max-w-sm mx-auto">
      <div className="bg-card rounded-3xl p-6 shadow-2xl border border-border">
        {/* Python Logo Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <div className="flex gap-0.5">
              <div className="w-4 h-4 rounded-full bg-secondary" />
              <div className="w-4 h-4 rounded-full bg-primary" />
            </div>
            <span className="font-mono text-sm text-muted-foreground">Python Calculator</span>
          </div>
          <button 
            onClick={handleDelete}
            className="p-2 rounded-lg hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
          >
            <Delete className="size-5" />
          </button>
        </div>

        {/* Display */}
        <div className="bg-muted rounded-2xl p-4 mb-6">
          <div className="text-right">
            <p className="text-sm text-muted-foreground font-mono h-5 truncate">
              {expression || ">>>"}
            </p>
            <p className="text-4xl font-bold font-mono text-foreground truncate">
              {display}
            </p>
          </div>
        </div>

        {/* Button Grid */}
        <div className="grid grid-cols-4 gap-3">
          {buttons.map((btn, index) => (
            <Button
              key={index}
              onClick={btn.action}
              className={`
                h-16 text-xl font-semibold rounded-xl transition-all active:scale-95
                ${btn.span ? "col-span-2" : ""}
                ${btn.variant === "secondary" 
                  ? "bg-muted hover:bg-muted/80 text-foreground" 
                  : btn.variant === "accent"
                  ? "bg-secondary hover:bg-secondary/80 text-secondary-foreground"
                  : btn.variant === "primary"
                  ? "bg-primary hover:bg-primary/90 text-primary-foreground"
                  : "bg-card hover:bg-muted text-foreground border border-border"
                }
              `}
            >
              {btn.label}
            </Button>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-6 text-center">
          <p className="text-xs text-muted-foreground font-mono">
            {">>> print('Hello, World!')"}
          </p>
        </div>
      </div>
    </div>
  )
}
